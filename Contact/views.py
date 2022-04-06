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
        data['contact_id'] = get_contact_id(data['contact_type'])
        contact = Contact(company=company, **data)
        contact.save()
        return Response({"message": "Contact Created."}, status=status.HTTP_201_CREATED)


'''

'''


class ContactUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ContactSerializer

    def update(self, request, contact_id, partial=True):
        company = self.request.company
        serializer = ContactUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if Contact.objects.filter(pk=contact_id, company=company).exists():
            oldContact = Contact.objects.filter(pk=contact_id, company=company).first()
            if not oldContact.contact_type.id == data['contact_type'].id:
                if Contact.objects.filter(nif=data['nif']).exists():
                    return Response({"message": "nif must be unique"}, status=status.HTTP_205_RESET_CONTENT)
                data['contact_id'] = get_contact_id(data['contact_type'])
                contact = Contact(company=company, **data)
                contact.save()
                oldContact.delete()
                return Response({"message": "Contact Updated"}, status=status.HTTP_200_OK)
            if not oldContact.nif == data['nif']:  # checking if nif is same as previous nif
                # if nif is new then checking if no other employe have the same nif
                if Contact.objects.filter(nif=data['nif']).exists():
                    return Response({"message": "nif must be unique"}, status=status.HTTP_205_RESET_CONTENT)
            contact = Contact(pk=contact_id, company=company, **data)
            contact.save()
            return Response({"message": "Contact Updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)


'''
update
'''


class ContactListAPIView(CompanyPermissionsMixin, generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = ContactSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ContactFilter

    def get_queryset(self):
        return Contact.objects.filter(company=self.request.company)


'''
Contact delete API View
'''


class ContactsdeleteAPIView(CompanyPermissionsMixin, generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCompanyAccess)
    serializer_class = ContactDeleteSerializer

    def delete(self, request, format=None):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        for id in data['contact_list']:
            if Contact.objects.filter(pk=id).filter(company=self.request.company).exists():
                instance = Contact.objects.get(pk=id)
                instance.delete()
            continue
        return Response(status=status.HTTP_204_NO_CONTENT)
