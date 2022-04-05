from .models import Contact
from rest_framework import status
from rest_framework.response import Response
from Core.models import Company, CompanyAccessRecord
from django.shortcuts import get_object_or_404
import random


'''
This method is due to because at 4 places same functionality was getting
used so to make code more readable and to remove duplication this method
created. Method recieving compani_id and current user and we are checing
if user have permissions for the requested company.
'''


def get_company_if_authenticated(user, company_id):
    response = Response(
        {"message": "Company not found"},
        status=status.HTTP_404_NOT_FOUND)
    if (user.is_staff and Company.objects.filter(
            pk=company_id, user=user).exists()) or \
        CompanyAccessRecord.objects.filter(
            user=user, company_id=company_id):
        return get_object_or_404(Company, pk=company_id)
    else:
        return response


def get_contact_id(contact_type):
    contact_type_name = contact_type.lookup_name.lower()
    if contact_type_name == "client":
        random_num = random.randint(430000000001, 439999999999)
        while Contact.objects.filter(contact_id=random_num).exists():
            random_num = random.randint(430000000001, 439999999999)
        return random_num

    elif contact_type_name == "debitor":
        random_num = random.randint(440000000001, 449999999999)
        while Contact.objects.filter(contact_id=random_num).exists():
            random_num = random.randint(440000000001, 449999999999)
        return random_num

    elif contact_type_name == "provider":
        random_num = random.randint(400000000001, 409999999999)
        while Contact.objects.filter(contact_id=random_num).exists():
            random_num = random.randint(400000000001, 409999999999)
        return random_num

    elif contact_type_name == "creditor":
        random_num = random.randint(410000000001, 419999999999)
        while Contact.objects.filter(contact_id=random_num).exists():
            random_num = random.randint(410000000001, 419999999999)
        return random_num

    else:
        return False
