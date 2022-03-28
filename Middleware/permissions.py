from rest_framework import permissions


class IsCompanyAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        company = False
        if request.company:
            company = True
        return (view.company_required and company)
