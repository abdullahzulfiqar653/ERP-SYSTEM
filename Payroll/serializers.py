from rest_framework import serializers
from .models import PayRoll, PayRollItem, PayrollTeam, Team, Employee


# ---------------------- Serializers for Team Views ---------------------------#
class TeamSerializer(serializers.ModelSerializer):
    country_label = serializers.CharField(read_only=True, source='country.lookup_name')
    has_employees = serializers.SerializerMethodField(read_only=True)

    def get_has_employees(self, team: Team):
        return True if Employee.objects.filter(team=team).exists() else False

    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'address',
            'postcode',
            'province',
            'country',
            'country_label',
            'note',
            'has_employees',
        ]


class TeamFormListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
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
    country_label = serializers.CharField(read_only=True, source='country.lookup_name')
    team_name = serializers.CharField(read_only=True, source='team.team_name')
    contract_type_label = serializers.CharField(read_only=True, source='contract_type.lookup_name')

    class Meta:
        model = Employee
        exclude = ['company', ]


class FormListEmployeeSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(read_only=True, source='team.id')
    name = serializers.SerializerMethodField()

    def get_name(self, employee: Employee):
        return '{} {}'.format(employee.name, employee.surname)

    class Meta:
        model = Employee
        fields = [
            'id',
            'team_id',
            'name',
            'current_salary'
        ]


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
    teams_list = serializers.ListField(child=serializers.IntegerField())

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
            'payroll_items',
            'teams_list',
        ]


class PayRollItemUpdateSerializer(serializers.ModelSerializer):
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


class PayRollUpdateSerializer(serializers.ModelSerializer):
    payroll_items = PayRollItemUpdateSerializer(many=True)
    teams_list = serializers.ListField(child=serializers.IntegerField())

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
            'payroll_items',
            'teams_list'
        ]


class PayrollsDeleteSerializer(serializers.ModelSerializer):
    payrolls_list = serializers.ListField(child=serializers.IntegerField(required=True))

    class Meta:
        model = PayRoll
        fields = [
            'payrolls_list'
        ]


class PayrollRelatedPayRollItemListSerializer(serializers.ModelSerializer):
    irfp_percent = serializers.DecimalField(
        source='irfp.irfp', read_only=True, max_digits=5, decimal_places=3)
    employee_name = serializers.SerializerMethodField()

    def get_employee_name(self, item: PayRollItem):
        return '{} {}'.format(item.employee.name, item.employee.surname)

    class Meta:
        model = PayRollItem
        exclude = ['payroll', ]


class PayrollTeamListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayrollTeam
        exclude = ['payroll', ]


# This Serializer is to return payroll instance including the related payroll Items.
class FetchPayrollSerializer(serializers.ModelSerializer):
    payroll_items = PayrollRelatedPayRollItemListSerializer(read_only=True, many=True)
    teams_list = PayrollTeamListSerializer(read_only=True, many=True)

    class Meta:
        model = PayRoll
        exclude = ['company']
        # fields = [
        #     'created_at',
        #     'payroll_items',
        #     'teams_list',
        #     'creation_date',
        #     'gross',
        #     'bonus',
        #     'total_gross',
        #     'irfp',
        #     'irfp_total',
        #     'ss_employee',
        #     'net',
        #     'ss_company',
        #     'discount',
        #     'company_cost',
        # ]


# This Serializer is to return only payroll instances not the related payroll Items.
class PayRollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRoll
        exclude = ['company', ]
