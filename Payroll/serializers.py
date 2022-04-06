from rest_framework import serializers
from .models import PayRoll, PayRollItem, Team, Employee, Contact, LookupType, LookupName, Tax


# ---------------------- Serializers for Team Views ---------------------------#
class TeamSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(read_only=True, source='country.lookup_name')

    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'address',
            'postcode',
            'province',
            'country',
            'country_name',
            'note',
        ]


class TeamsDeleteSerializer(serializers.ModelSerializer):
    teams_list = serializers.ListField(child=serializers.IntegerField(required=True))

    class Meta:
        model = Team
        fields = [
            'teams_list'
        ]


# ---------------------- Serializers for Employee Views ---------------------------#
class AddEmployeeSerializer(serializers.ModelSerializer):
    team = serializers.IntegerField(required=True)
    nif = serializers.CharField(validators=[], )

    class Meta:
        model = Employee
        fields = [
            'team',
            'name',
            'surname',
            'nif',
            'social_security',
            'address',
            'contract_type',
            'enddate',
            'current_salary',
            'postcode',
            'province',
            'country',
            'note',
        ]


class ListEmployeeSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(read_only=True, source='country.lookup_name')

    class Meta:
        model = Employee
        exclude = ['company', ]


class EmployeesDeleteSerializer(serializers.ModelSerializer):
    employees_list = serializers.ListField(child=serializers.IntegerField(required=True))

    class Meta:
        model = Employee
        fields = [
            'employees_list'
        ]


# ---------------------- Serializers for Payroll Views ---------------------------#
class PayRollItemSerializer(serializers.ModelSerializer):
    employee = serializers.IntegerField(required=True)

    class Meta:
        model = PayRollItem
        fields = [
            'employee',
            'gross',
            'bonus',
            'total_gross',
            'irfp',
            'irfp_total',
            'ss_employee',
            'net',
            'ss_company',
            'discount',
            'company_cost'
        ]


class PayRollCreateSerializer(serializers.ModelSerializer):
    payroll_items = PayRollItemSerializer(many=True)

    class Meta:
        model = PayRoll
        fields = [
            'created_at',
            'gross',
            'bonus',
            'total_gross',
            'irfp',
            'irfp_total',
            'ss_employee',
            'net',
            'ss_company',
            'discount',
            'company_cost',
            'payroll_items'
        ]


class PayRollItemUpdateSerializer(serializers.ModelSerializer):
    employee = serializers.IntegerField(required=True)
    id = serializers.IntegerField(required=True)

    class Meta:
        model = PayRollItem
        fields = [
            'id',
            'employee',
            'gross',
            'bonus',
            'total_gross',
            'irfp',
            'irfp_total',
            'ss_employee',
            'net',
            'ss_company',
            'discount',
            'company_cost'
        ]


class PayRollUpdateSerializer(serializers.ModelSerializer):
    payroll_items = PayRollItemUpdateSerializer(many=True)
    id = serializers.IntegerField(required=True)

    class Meta:
        model = PayRoll
        fields = [
            'id',
            'created_at',
            'gross',
            'bonus',
            'total_gross',
            'irfp',
            'irfp_total',
            'ss_employee',
            'net',
            'ss_company',
            'discount',
            'company_cost',
            'payroll_items'
        ]


class PayrollRelatedPayRollItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRollItem
        exclude = ['payroll', ]


class PayrollsDeleteSerializer(serializers.ModelSerializer):
    payrolls_list = serializers.ListField(child=serializers.IntegerField(required=True))

    class Meta:
        model = PayRoll
        fields = [
            'payrolls_list'
        ]


# This Serializer is to return payroll instance including the related payroll Items.
class FetchPayrollSerializer(serializers.ModelSerializer):
    payroll_items = PayrollRelatedPayRollItemListSerializer(read_only=True, many=True)

    class Meta:
        model = PayRoll
        exclude = ['company']


# This Serializer is to return only payroll instances not the related payroll Items.
class PayRollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRoll
        exclude = ['company', ]


# ---------------------- Serializers for Contact Module ---------------------------#
class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id',
            'contact_type',
            'name',
            'nif',
            'tax_address',
            'tax_postcode',
            'tax_province',
            'tax_country',
            'shipping_address',
            'shipping_postcode',
            'shipping_province',
            'shipping_country',
            'account_type',
            'vat',
            'ret_or_equiv',
            'payment_method',
            'payment_extension',
        ]


class ContactUpdateSerializer(serializers.ModelSerializer):
    nif = serializers.CharField(validators=[],)

    class Meta:
        model = Contact
        fields = [
            'contact_type',
            'name',
            'nif',
            'tax_address',
            'tax_postcode',
            'tax_province',
            'tax_country',
            'shipping_address',
            'shipping_postcode',
            'shipping_province',
            'shipping_country',
            'account_type',
            'vat',
            'ret_or_equiv',
            'payment_method',
            'payment_extension',
        ]


'''
serializer to accept list of company id's
'''


class ContactDeleteSerializer(serializers.ModelSerializer):
    contact_list = serializers.ListField(child=serializers.IntegerField(required=True))

    class Meta:
        model = Contact
        fields = [
            'contact_list'
        ]


# ---------------------------------------------------------------------------------#
# ---------------------- Serializers for Lookups Module ---------------------------#
# ---------------------------------------------------------------------------------#
class LookupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookupType
        fields = ['lookup_type']


class LookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookupName
        fields = [
            'id',
            'lookup_name',
        ]


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        exclude = ['lookup_name', ]
