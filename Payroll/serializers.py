from rest_framework import serializers
from .models import PayRoll, PayRollItem, Team, Employee, Contact


# ---------------------- Serializers for Team Views ---------------------------#
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'team_name',
            'address',
            'postcode',
            'province',
            'country',
            'note',
        ]


class RetriveTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'address',
            'postcode',
            'province',
            'country',
            'note',
        ]


# ---------------------- Serializers for Employee Views ---------------------------#
class AddEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = [
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


class UpdateEmployeeSerializer(serializers.ModelSerializer):
    nif = serializers.CharField(validators=[], )

    class Meta:
        model = Employee
        fields = [
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
    class Meta:
        model = Employee
        fields = [
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


# ---------------------- Serializers for Payroll Views ---------------------------#
class PayRollItemSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(required=True, write_only=True, source='employee')

    class Meta:
        model = PayRollItem
        fields = [
            'employee_id',
            'gross',
            'bonus',
            'total_gross',
        ]


class PayRollCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(required=True, write_only=True, source='company')
    payroll_items = PayRollItemSerializer(many=True)

    class Meta:
        model = PayRoll
        fields = [
            'company_id',
            'created_at',
            'payroll_items'
        ]


class PayRollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRoll
        fields = [
            'id',
            'created_at',
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'name',
        ]


class PayRollItemListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = PayRollItem
        fields = [
            'id',
            'employee',
            'gross',
            'bonus',
            'total_gross',
        ]


class PayRollItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRollItem
        fields = [
            'gross',
            'bonus',
            'total_gross',
        ]


# Contact, ContactTaxAddress, ContactShipAddress, ContactPayment
# ---------------------- Serializers for Contact Module ---------------------------#
class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id',
            'type',
            'name',
            'account_id',
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
            'ret_or_re',
            'payment_method',
            'date',
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
