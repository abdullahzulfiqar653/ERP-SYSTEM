from django.contrib.auth.models import User
# from django_filters
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import (
    AddTeamSerializer,
    RetriveTeamSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .models import Team
from utils.pagination import LimitOffsetPagination
from Core.models import Company, CompanyAccessRecord
from .filters import TeamFilter

'''This View is for creating a team and admin or any subusers who have permissions to access
company can create team in that company. This View first check if user is admin and create team
request is in his companies then its a valid request So by validating other parameters team will
be created against requested company. If user is not admin then check if team creation request for
a comapny is in his access records then after validating other parametrs team will be created
against requested company.
'''
class AddTeamView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddTeamSerializer
    def post(self, request, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        response = Response(status=status.HTTP_400_BAD_REQUEST)
        if data.get('company_id') and Company.objects.filter(pk=data.get('company_id')).exists():
            if user.is_staff and Company.objects.filter(pk=int(data.get('company_id'))).filter(user=user).exists():
                company = Company.objects.get(pk=int(data.get('company_id')))
            elif CompanyAccessRecord.objects.filter(user=user, company_id=data.get('company_id')):
                company = Company.objects.get(pk=int(data.get('company_id')))
            else:
                return response
        else:
            return response
        
        if data.get("team_name") and not Team.objects.filter(company=company).filter(team_name=data.get("team_name")).exists():
            team = Team.objects.create(
                company = company,
                team_name = data.get("team_name"),
                address = data.get("address"),
                postcode = data.get("postcode"),
                province = data.get("province"),
                country = data.get("country"),
                note = data.get("note")
                )
            return Response({'message': "Team {} created against {}.".format(team.team_name, company.name)}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_205_RESET_CONTENT)


'''This View is for updating any team after some validations user or admin user can update his team,
but user is limited to only those teams which he have permissions to Access.'''
class UpdateTeamView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddTeamSerializer
    def update(self, request, id):
        team_id = id
        data = self.request.data
        user = self.request.user

        if Team.objects.filter(pk=team_id).exists(): #Checking if Team Exists in database.
            team = Team.objects.get(pk=team_id)  #getting Current Team.    
            company = Company.objects.filter(pk=team.company.id) #Getting company related to current team for next use
            if user.is_staff:   #checking if user is a admin user.
                if not company.filter(user=user).exists():  #veryfying if admin owns the company or not
                    return Response(status=status.HTTP_401_UNAUTHORIZED)   
            elif not CompanyAccessRecord.objects.filter(user=user, company=company.first()).exists():   #veryfying if sub_user owns the company or not
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if data.get("team_name"): #checking if team name exists()
            if not team.team_name == data.get("team_name"): # Checking if current team has the same name then ignoring next conditions
                if Team.objects.filter(company=company.first(), team_name=data.get("team_name")).exists(): #veryfying uniqness in current company
                    return Response({"messgae": "Team name must be unique"}, status=status.HTTP_205_RESET_CONTENT)
            team.team_name = data.get("team_name")
            team.address = data.get("address")
            team.postcode = data.get("postcode")
            team.province = data.get("province")
            team.country = data.get("country")
            team.note = data.get("note")
            team.save()

            return Response({'success': "Team {} updated".format(team.team_name)}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_205_RESET_CONTENT)


'''
Team Listing view having a parameter in the URL as company_id and then veryfying if current
user owns the company or have permission to access the company if yes then returning teams related to those users.
'''
class TeamListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RetriveTeamSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TeamFilter
    def get_queryset(self):
        company_id = self.request.GET.get('company_id')
        empty_queryset = Team.objects.none()
        if not company_id:
            return empty_queryset
        if not company_id.isdigit():
            return empty_queryset
        user = self.request.user
        if user.is_staff and Company.objects.filter(pk=int(company_id)).filter(user=user).exists():
            return Team.objects.filter(company=company_id)
        elif CompanyAccessRecord.objects.filter(user=user, company_id=company_id).exists():
            return Team.objects.filter(company=company_id)
        else:
            return empty_queryset



class TeamDestroyView(generics.DestroyAPIView):
    queryset = Team.objects.all()
    permission_class = (permissions.IsAuthenticated,)
    def perform_destroy(self, instance):
        user = self.request.user
        team = Team.objects.filter(pk=instance.id).first()
        print(isinstance(team.company, Company))
        if user.is_staff and team.company.user==user:
            super().perform_destroy(instance)
        elif CompanyAccessRecord.objects.filter(user=user, company=team.company).exists():
            super().perform_destroy(instance)
        else:
            return {"message": "you are an unauthorized user to perform this action"}