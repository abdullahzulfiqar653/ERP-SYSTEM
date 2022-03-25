from django_filters import FilterSet
from .models import Team, Employee, PayRoll, Contact


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


class PayRollFilter(FilterSet):
    class Meta:
        model = PayRoll
        fields = {
            "created_at": ['year', 'month'],
        }


class ContactFilter(FilterSet):
    class Meta:
        model = Contact
        fields = {
            "type": ['iexact'],
            "name": ['iexact'],
            "account_id": ['exact'],
            "nif": ['exact'],

            "tax_address": ['icontains'],
            "tax_postcode": ['exact'],
            "tax_province": ['iexact'],
            "tax_country": ['iexact'],

            "shipping_address": ['icontains'],
            "shipping_postcode": ['exact'],
            "shipping_province": ['iexact'],
            "shipping_country": ['iexact'],

            "account_type": ['iexact'],
            "vat": ['exact'],
            "ret_or_re": ['exact'],
            "payment_method": ['icontains'],
            "date": ['year', 'month', 'day'],
        }
