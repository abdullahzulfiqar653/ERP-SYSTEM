from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .utils import get_company_if_authenticated
from .serializers import (
    TeamSerializer,
    AddEmployeeSerializer,
    ListEmployeeSerializer,
    PayRollCreateSerializer,
    FetchPayrollSerializer,
    PayRollListSerializer,
    PayRollUpdateSerializer,
    ContactSerializer,
    ContactDeleteSerializer,
    LookupTypeSerializer,
    LookupSerializer,
    TaxSerializer,
)
from .models import Tax, Team, Employee, PayRoll, PayRollItem, Contact, LookupType, LookupName
from utils.pagination import LimitOffsetPagination
from Core.models import Company
from .filters import TeamFilter, EmployeeFilter, PayRollFilter, ContactFilter
from Middleware.CustomMixin import CompanyPermissionsMixin
from Middleware.permissions import IsCompanyAccess
# ---------------------- Starting Crud for Team ---------------------------#

'''
This View is for creating a team and admin or any subusers who have
permissions to access company can create team in that company. This
View first check if user is admin and create team request is in his
companies then its a valid request So by validating other parameters
team will be created against requested company. If user is not admin
then check if team creation request for a comapny is in his access
records then after validating other parametrs team will be created
against requested company.
'''


class AddTeamView(CompanyPermissionsMixin, generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = TeamSerializer

    def post(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        company = self.request.company

        if not Team.objects.filter(company=company, team_name=data["team_name"]).exists():
            team = Team(company=company, **data)
            team.save()
            return Response({'message': "Team {} created against {}.".format(
                team.team_name, company.name), "team": TeamSerializer(team).data}, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "Enter Unique Team name"},
            status=status.HTTP_205_RESET_CONTENT)


'''
This View is for updating any team after some validations user or admin
user can update his team, but user is limited to only those teams which
he have permissions to Access.
'''


class UpdateTeamView(CompanyPermissionsMixin, generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = TeamSerializer

    def update(self, request, team_id):
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        company = self.request.company

        # Checking if Team Exists in database.
        if Team.objects.filter(pk=team_id, company=company).exists():
            team = Team.objects.get(pk=team_id)  # getting Current Team.
        else:
            return Response(
                {"message": "Team not Found"},
                status=status.HTTP_404_NOT_FOUND)

        if not team.team_name == data["team_name"]:  # Checking if current team has the same name then ignoring next conditions
            if Team.objects.filter(company=company, team_name=data["team_name"]).exists():  # veryfying uniqness in current company
                return Response({"messgae": "Team name must be unique"}, status=status.HTTP_205_RESET_CONTENT)
        team = Team(pk=team.id, company=company, **data)
        team.save()
        return Response(
            {'message': "Team {} updated".format(team.team_name),
                "team": TeamSerializer(team).data}, status=status.HTTP_200_OK
                )


'''
Team Listing view having a parameter in the URL as company_id and then veryfying if current
user owns the company or have permission to access the company if yes then returning teams
related to those users.
'''


class TeamListView(CompanyPermissionsMixin, generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = TeamSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TeamFilter
    ordering_fields = ['id', 'team_name']

    def get_queryset(self):
        company = self.request.company
        return Team.objects.filter(company=company)


'''
This View have an id of Team in the URL params by that it fetch the
instance of team and after checking some permissions it destroy that instance
'''


class TeamDestroyView(CompanyPermissionsMixin, generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)

    def get_queryset(self):
        return Team.objects.filter(company=self.request.company)


# ---------------------- Starting Crud for Employee ---------------------------#

'''
This view is For creating an employee. After request this view firstly validate
data through serializer and then check if user request is valid to create an
employee in requested company by calling method get_company_if_authenticated
if company is returned then its mean user have permission to create Employe
in requested company, and employee will be created. Else HTTP_400_BAD_REQUEST
will be returned.
'''


class EmployeeCreateAPIView(CompanyPermissionsMixin, generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = AddEmployeeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        company = self.request.company
        if not Team.objects.filter(pk=data["team"], company=company).exists():
            return Response({"message": "Team not Found"}, status=status.HTTP_404_NOT_FOUND)
        if Employee.objects.filter(nif=data['nif']).exists():
            return Response({"message": "nif must be unique"}, status=status.HTTP_205_RESET_CONTENT)
        team_id = data["team"]
        del data["team"]
        employee = Employee(company=company, team_id=team_id, **data)
        employee.save()

        return Response({'message': "Employee {} created against {}.".format(
            employee.name, company.name), "employee": ListEmployeeSerializer(employee).data},
            status=status.HTTP_201_CREATED
            )


'''
this View overriding the base get_queryset method and in that before
filtering it check weather the user requesting for employees for a
company own the company or have permissions to access that company
the Employess related to the requested company. user own the company
or have permissions to access that company then only employees related
to accessed company will be returned. This View Also containing Pagination
and Filters to filter specific data.
'''


class EmployeeListAPIView(CompanyPermissionsMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCompanyAccess]
    serializer_class = ListEmployeeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EmployeeFilter
    ordering_fields = ['id', 'name']

    def get_queryset(self):
        return Employee.objects.filter(company=self.request.company)


'''
This View on request first check if user have permissions to the company
or not if yess then check if employee is the employee of the requested
company. After that it check if nif of user is same as previous then nif
get poped and other data will be updated otherwise check if new nif is
not belong to any existing user if not then all data of employee will be
updated.
'''


class EmployeeUpdateView(CompanyPermissionsMixin, generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = AddEmployeeSerializer

    def update(self, request, emp_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        company = self.request.company
        if not (Employee.objects.filter(pk=emp_id, company=company).exists()
                and Team.objects.filter(pk=data["team"], company=company).exists()):
            return Response(
                {'message': "team or employee not found"}, status=status.HTTP_404_NOT_FOUND)

        emp = Employee.objects.get(pk=emp_id, company=company)
        team_id = data["team"]
        del data["team"]
        if not emp.nif == data['nif']:  # checking if nif is same as previous nif
            # if nif is new then checking if no other employe have the same nif
            if Employee.objects.filter(nif=data['nif']).exists():
                return Response({"message": "nif must be unique"}, status=status.HTTP_205_RESET_CONTENT)
        emp = Employee(pk=emp.id, company=company, team_id=team_id, **data)
        emp.save()
        return Response({'message': "Employee {} updated".format(emp.name)}, status=status.HTTP_200_OK)


'''
Checking if user have permissions to the requested company and
also employee related to that companny then employee will be deleted
'''


class EmployeeDestroyView(CompanyPermissionsMixin, generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)

    def get_queryset(self):
        return Employee.objects.filter(company=self.request.company)


# ---------------------- Starting Crud for PayRoll ---------------------------#
'''
In this View first of all view are validating the payload through calling
the serializer and then after that we are calling method to check if current
user have permissions to perform create payRoll if in return. I get a instance
of Company then we create Payroll and start loop to create its Items. In each
iteration first it check if employee id belongs to current company if yes then
Payroll Item will be created.
'''


class PayRollCreateAPIView(CompanyPermissionsMixin, generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = PayRollCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        company = self.request.company
        payroll_items = data['payroll_items']
        del data['payroll_items']
        payroll = PayRoll.objects.create(company=company, **data)

        for item in payroll_items:
            if Employee.objects.filter(pk=item['employee'], company=company).exists():
                item['employee_id'] = item['employee']
                del item['employee']
                PayRollItem.objects.create(
                    payroll=payroll,
                    **item,
                    )
            continue
        return Response({"payroll": PayRollListSerializer(payroll).data}, status=status.HTTP_201_CREATED)


'''
Here this view is for returning all the payrolls related to the requested company
only if user have permissions for the company or he/she owns the company then all
related Payrolls will be returned. also pagination is attached to control pages or
unlimited objects per page.
'''


class PayRollListAPIView(CompanyPermissionsMixin, generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = PayRollListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = PayRollFilter

    def get_queryset(self):
        return PayRoll.objects.all()


'''
This View is use for returning Payroll Items related to any One payroll.
'''


class PayRollItemListAPIView(CompanyPermissionsMixin, generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = FetchPayrollSerializer

    def get_queryset(self):
        return PayRoll.objects.filter(company=self.request.company)


'''
Here updating payroll Item by firstly checking if payroll exists() then get pay
roll and then check if payroll company permissions are assigned to current user
or not if yess then it simply update all parameters related to the payroll item.
'''


class PayRollItemUpdateAPIView(CompanyPermissionsMixin, generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = PayRollUpdateSerializer

    def update(self, request, payroll_id, partial=True):
        company = self.request.company
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        company = self.request.company
        payroll_items = data['payroll_items']
        del data['payroll_items']
        if not PayRoll.objects.filter(pk=payroll_id, company=company).exists():
            return Response({"message": "Payroll not found"}, status=status.HTTP_404_NOT_FOUND)
        payroll = PayRoll(pk=payroll_id, company=company, **data)
        payroll.save()

        for item in payroll_items:
            if Employee.objects.filter(pk=item['employee'], company=company).exists() and \
                    PayRollItem.objects.filter(pk=item['id'], payroll=payroll).exists():
                item['employee_id'] = item['employee']
                del item['employee']
                payrollItem = PayRollItem(pk=item['id'], payroll=payroll, **item,)
                payrollItem.save()
            continue
        return Response(
            {"message": "Payroll Updated.", "payroll": PayRollListSerializer(payroll).data},
            status=status.HTTP_200_OK
            )


'''
This View get an id of payroll in the URL and check if user have permissions
to delete that payroll. If yess then payroll and related all payroll Items
will be deleted.
'''


class PayRollDestroyView(CompanyPermissionsMixin, generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)

    def get_queryset(self):
        return PayRoll.objects.filter(company=self.request.company)


'''
Same as before but here we are deleting payroll item after veryfying the user permissions.
'''


class PayRollItemDestroyView(CompanyPermissionsMixin, generics.DestroyAPIView):
    queryset = PayRollItem.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)

    def perform_destroy(self, instance):
        payroll = PayRoll.objects.filter(pk=instance.payroll_id).first()
        company = self.request.company
        if PayRoll.objects.filter(pk=payroll.id, company=company).exists():
            super().perform_destroy(instance)


# ---------------------- Starting Crud for Contact ---------------------------#
class ContactCreateAPIView(CompanyPermissionsMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCompanyAccess]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        company_id = self.request.GET.get('company_id')
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = self.request.user
        company = get_company_if_authenticated(user, company_id)
        if not isinstance(company, Company):
            return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        contact = Contact(company=company, **data)
        contact.save()
        return Response({"message": "Contact Created."}, status=status.HTTP_201_CREATED)


'''

'''


class ContactUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ContactSerializer

    def update(self, request, contact_id, partial=True):
        company_id = self.request.GET.get('company_id')
        # contact_id = self.request.GET.get('contact_id')
        user = self.request.user
        company = get_company_if_authenticated(user, company_id)
        if not isinstance(company, Company):
            return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if Contact.objects.filter(pk=contact_id, company=company).exists():
            contact = Contact.objects.filter(pk=contact_id, company=company).first()
            contact.type = data["type"]
            contact.name = data["name"]
            contact.account_id = data["account_id"]
            contact.nif = data["nif"]
            contact.tax_address = data["tax_address"]
            contact.tax_postcode = data["tax_postcode"]
            contact.tax_province = data["tax_province"]
            contact.tax_country = data["tax_country"]
            contact.shipping_address = data["shipping_address"]
            contact.shipping_postcode = data["shipping_postcode"]
            contact.shipping_province = data["shipping_province"]
            contact.shipping_country = data["shipping_country"]
            contact.account_type = data["account_type"]
            contact.vat = data["vat"]
            contact.ret_or_re = data["ret_or_re"]
            contact.payment_method = data["payment_method"]
            contact.date = data["date"]
            contact.save()
            return Response({"message": "Contact Updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)


'''
update
'''


class ContactListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContactSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ContactFilter

    def get_queryset(self):
        company_id = self.request.GET.get('company_id')
        emptyContactQueryset = Contact.objects.none()
        user = self.request.user
        company = get_company_if_authenticated(user, company_id)
        if not isinstance(company, Company):
            return emptyContactQueryset
        return Contact.objects.filter(company=company)


'''
Contact delete API View
'''


class ContactsdeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, format=None):
        serializer = ContactDeleteSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data['contact_list']:
            company_id = self.request.GET.get('company_id')
            user = self.request.user
            company = get_company_if_authenticated(user, company_id)
            if not isinstance(company, Company):
                return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

            for id in data['contact_list']:
                if Contact.objects.filter(pk=id).filter(company=company).exists():
                    instance = Contact.objects.get(pk=id)
                    instance.delete()
                continue
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# ---------------------------------------------------------------------------------#
# ---------------------- Views for Lookups Module ---------------------------------#
# ---------------------------------------------------------------------------------#
class LookupTypeListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LookupTypeSerializer
    queryset = LookupType.objects.all()


class LookupListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LookupSerializer

    def get_queryset(self):
        return LookupName.objects.filter(lookup_type__lookup_type=self.kwargs['lookup'])


class TaxListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TaxSerializer

    def get_queryset(self):
        if "client" == self.kwargs['lookup'].lower() or "debitor" == self.kwargs['lookup'].lower():
            return Tax.objects.filter(lookup_name__lookup_name=self.kwargs['lookup'].lower()).values('id', 'vat', 'equiv')
        if "provider" == self.kwargs['lookup'].lower() or "creditor" == self.kwargs['lookup'].lower():
            return Tax.objects.filter(lookup_name__lookup_name=self.kwargs['lookup'].lower()).values('id', 'vat', 'ret')
        if "payrolltax" == self.kwargs['lookup'].lower():
            return Tax.objects.filter(lookup_name__lookup_name=self.kwargs['lookup'].lower()).values('id', 'irfp')
        return Tax.objects.all()
