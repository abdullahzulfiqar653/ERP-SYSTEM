from django_filters import FilterSet
from .models import Team

class TeamFilter(FilterSet):
    class Meta:
        model = Team
        fields = {
            "team_name": ['iexact'],
            "address": ['icontains'],
            "postcode": ['exact'],
            "province": ['iexact'],
            "country": ['iexact'],
            "note": ['icontains'],
        }