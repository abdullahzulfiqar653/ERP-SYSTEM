from django_filters import FilterSet
from .models import Team, Employee

class TeamFilter(FilterSet):
    class Meta:
        model = Team
        fields = {
            "team_name": ['iexact'],
            "address": ['icontains'],
            "postcode": ['exact'],
            "province": ['iexact'],
            "country": ['iexact'],
            "note": ['icontains'],
        }


class EmployeeFilter(FilterSet):
    class Meta:
        model = Employee
        fields = {
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
            "country": ['iexact'],
            "note": ['icontains'],
        }