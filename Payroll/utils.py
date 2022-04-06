
from rest_framework import status
from rest_framework.response import Response
from Core.models import Company, CompanyAccessRecord
from django.shortcuts import get_object_or_404


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
