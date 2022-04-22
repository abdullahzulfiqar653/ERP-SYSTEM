from django.contrib import admin
from .models import (
    Team,
    Employee,
    PayRoll,
    PayRollItem,
    PayrollTeam
)
# Register your models here.


class TeamAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'team_name',
        'company',
        'creation_year'
    ]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'nif',
        'team',
        'company',
        'creation_year'
    ]


class PayRollItemAdmin(admin.TabularInline):
    model = PayRollItem
    extra = 0


class PayRollTeamAdmin(admin.ModelAdmin):
    # model = PayrollTeam
    # extra = 0
    list_display = ['payroll', 'team']


class PayRollAdmin(admin.ModelAdmin):
    inlines = [PayRollItemAdmin, ]
    list_display = ['id', 'created_at_year', 'creation_year']


admin.site.register(Team, TeamAdmin)
admin.site.register(PayrollTeam, PayRollTeamAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PayRoll, PayRollAdmin)
