from django.contrib import admin
from .models import Team
# Register your models here.


class TeamAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'team_name',
        'company'
    ]

admin.site.register(Team, TeamAdmin)