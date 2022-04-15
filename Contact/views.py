from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from Middleware.CustomMixin import CompanyPermissionsMixin
from Middleware.permissions import IsCompanyAccess
from utils.pagination import LimitOffsetPagination
from .utils import get_contact_id
from .models import Contact
from .filters import ContactFilter
from .serializers import (
    ContactSerializer,
    ContactListSerializer,
    ContactUpdateSerializer,
    ContactDeleteSerializer,
)


# Create your views here.
# ---------------------- Starting Crud for Contact ---------------------------#
class ContactCreateAPIView(CompanyPermissionsMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCompanyAccess]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        company = self.request.company
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if Contact.objects.filter(nif=data['nif'], company=company).exists():
            return Response({"nif": "NIF already exists."}, status=status.HTTP_400_BAD_REQUEST)
        data['contact_id'] = get_contact_id(data['contact_type'])
        contact = Contact(company=company, **data)
        contact.save()
        return Response({
            "message": "Contact Created.",
            "contact": ContactSerializer(contact).data},
            status=status.HTTP_201_CREATED)


'''
update
'''


class ContactUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def update(self, request, contact_id, partial=True):
        company = self.request.company
        serializer = ContactUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not Contact.objects.filter(pk=contact_id, company=company).exists():
            return Response({"message": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)
        oldContact = Contact.objects.filter(pk=contact_id, company=company).first()

        if not oldContact.nif == data['nif']:  # checking if nif is same as previous nif
            # if nif is new then checking if no other employe have the same nif
            if Contact.objects.filter(nif=data['nif'], company=company).exists():
                return Response({"nif": "NIF already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if not oldContact.contact_type.id == data['contact_type'].id:
            data['contact_id'] = get_contact_id(data['contact_type'])
            contact = Contact(company=company, **data)
            contact.save()
            oldContact.delete()
        else:
            data['contact_id'] = oldContact.contact_id
            contact = Contact(pk=contact_id, company=company, **data)
            contact.save()
        return Response({
            "message": "Contact Updated",
            "contact": ContactSerializer(contact).data},
            status=status.HTTP_200_OK)


class ContactListAPIView(CompanyPermissionsMixin, generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = ContactListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ContactFilter

    def get_queryset(self):
        return Contact.objects.filter(company=self.request.company)


class ContactRetrieveAPIView(CompanyPermissionsMixin, generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(company=self.request.company)


'''
Contact delete API View
'''


class ContactsdeleteAPIView(CompanyPermissionsMixin, generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = ContactDeleteSerializer

    def delete(self, request, format=None):
        company = self.request.company
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        Contact.objects.filter(pk__in=data['contact_list'], company=company).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
