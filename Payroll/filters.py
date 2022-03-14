from django_filters import FilterSet
from .models import Team

class TeamFilter(FilterSet):
    class Meta:
        model = Team
        fields = {
            "team_name": ['exact'],
            "country": ['exact'],
            "address": ['exact'],
        }