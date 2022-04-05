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
            "country__lookup_name": ['iexact'],
            "note": ['icontains'],
        }


class EmployeeFilter(FilterSet):
    class Meta:
        model = Employee
        fields = {
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
            "country__lookup_name": ['iexact'],
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


class ContactFilter(FilterSet):
    class Meta:
        model = Contact
        fields = {
            "contact_type__lookup_name": ['iexact'],
            "name": ['iexact'],
            "contact_id": ['exact'],
            "nif": ['exact'],

            "tax_address": ['icontains'],
            "tax_postcode": ['exact'],
            "tax_province": ['iexact'],
            "tax_country__lookup_name": ['iexact'],

            "shipping_address": ['icontains'],
            "shipping_postcode": ['exact'],
            "shipping_province": ['iexact'],
            "shipping_country__lookup_name": ['iexact'],

            "account_type__english_name": ['iexact'],
            "vat": ['exact'],
            "ret_or_equiv": ['exact'],
            "payment_method__lookup_name": ['iexact'],
            "payment_extension__day": ['iexact'],
        }
