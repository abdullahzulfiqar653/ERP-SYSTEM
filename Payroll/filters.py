from django_filters import FilterSet
from .models import Team, Employee, PayRoll


class TeamFilter(FilterSet):
    class Meta:
        model = Team
        fields = {
            "team_name": ['icontains'],
            "address": ['icontains'],
            "postcode": ['exact'],
            "province": ['iexact'],
            "country__id": ['exact'],
            "note": ['icontains'],
        }


class EmployeeFilter(FilterSet):
    class Meta:
        model = Employee
        fields = {
            "id": ["exact"],
            "name": ['icontains'],
            "surname": ['icontains'],
            "contract_type": ['exact'],
            "enddate": ['exact'],
            "team": ["exact"],
            "current_salary": ['gt', 'lt'],
        }


class PayRollFilter(FilterSet):
    class Meta:
        model = PayRoll
        fields = {
            "id": ["exact"],
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
