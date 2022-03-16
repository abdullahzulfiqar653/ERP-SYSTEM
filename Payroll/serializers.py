from rest_framework import serializers
from .models import Team, Employee

#---------------------- Serializers for Team Views ---------------------------#
class AddTeamSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField()
    class Meta:
        model = Team
        fields = [
            'company_id',
            'team_name',
            'address',
            'postcode',
            'province',
            'country',
            'note',
        ]

class UpdateTeamSerializer(serializers.ModelSerializer):
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



#---------------------- Serializers for Employee Views ---------------------------#
class AddEmployeeSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField()
    class Meta:
        model = Employee
        fields = [
            'company_id',
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
    company_id = serializers.IntegerField()
    class Meta:
        model = Employee
        fields = [
            'company_id',
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