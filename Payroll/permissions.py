from asyncio.windows_events import NULL
from rest_framework import permissions
from Core.models import Company, CompanyAccessRecord
from django.contrib.auth.models import User

class IsCompanyAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        company_id = request.GET.get('company_id')
        if not company_id:
            return False
        if not company_id.isdigit():
            return False

        company = NULL
        user = request.user
        if not isinstance(user, User):
            return False
        if Company.objects.filter(pk=company_id).exists():  #check if Company exist or not
            if user.is_staff and Company.objects.filter(pk=company_id).filter(user=user).exists(): #if user is admin then check user own the company
                company = Company.objects.get(pk=company_id)
                return company
            elif CompanyAccessRecord.objects.filter(user=user, company_id=company_id):#if user is not admin then checking if user have access to the requested company
                company = Company.objects.get(pk=company_id)
                return company
            if isinstance(company, Company):
                True
        else:
            return False