from django.contrib import admin
from .models import Team, Employee
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
        'company'
    ]


admin.site.register(Team, TeamAdmin)
admin.site.register(Employee, EmployeeAdmin)