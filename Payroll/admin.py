from django.contrib import admin
from .models import (
    Team,
    Employee,
    PayRoll,
    PayRollItem,
    Contact,
    LookupType,
    LookupName,
    Tax,
    Payment_Day,
    AccountType,
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


class TaxAdmin(admin.ModelAdmin):
    list_display = ['id', 'lookup_name', 'vat', 'ret', 'equiv', 'irfp']


admin.site.register(Team, TeamAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PayRollItem)
admin.site.register(PayRoll)
admin.site.register(Contact)

admin.site.register(LookupName)
admin.site.register(LookupType)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Payment_Day)
admin.site.register(AccountType)
