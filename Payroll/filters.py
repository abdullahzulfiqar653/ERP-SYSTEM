from django_filters import FilterSet
from .models import Team, Employee, PayRoll


class TeamFilter(FilterSet):
    class Meta:
        model = Team
        fields = {
            "team_name": ['iexact'],
            "address": ['icontains'],
            "postcode": ['exact'],
            "province": ['iexact'],
            "country__lookup_name": ['iexact'],
            "note": ['icontains'],
        }


class EmployeeFilter(FilterSet):
    class Meta:
        model = Employee
        fields = {
            "id": ["exact"],
            "team__id": ["exact"],
            "name": ['iexact'],
            "surname": ['iexact'],
            "nif": ['exact'],
            "social_security": ['icontains'],
            "contract_type": ['exact'],
            "address": ['icontains'],
            "enddate": ['exact'],
            "current_salary": ['gt', 'lt'],
            "postcode": ['exact'],
            "province": ['iexact'],
            "country__id": ['exact'],
            "note": ['icontains'],
        }


class PayRollFilter(FilterSet):
    class Meta:
        model = PayRoll
        fields = {
            "created_at": ['year', 'month'],
            "gross": ['gt', 'lt'],
            "bonus": ['gt', 'lt'],
            "total_gross": ['gt', 'lt'],
            "irfp": ['gt', 'lt'],
            "irfp_total": ['gt', 'lt'],
            "ss_employee": ['gt', 'lt'],
            "net": ['gt', 'lt'],
            "ss_company": ['gt', 'lt'],
            "discount": ['gt', 'lt'],
            "company_cost": ['gt', 'lt']
        }
