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
        'company'
    ]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'nif',
        'team',
        'company'
    ]


class PayRollItemAdmin(admin.TabularInline):
    model = PayRollItem
    extra = 0


class PayRollTeamAdmin(admin.TabularInline):
    model = PayrollTeam
    extra = 0


class PayRollAdmin(admin.ModelAdmin):
    inlines = [PayRollItemAdmin, PayRollTeamAdmin]
    list_display = ['id', 'created_at']


admin.site.register(Team, TeamAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PayRoll, PayRollAdmin)
