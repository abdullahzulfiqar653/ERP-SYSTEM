
from django.db import models
from django.contrib.auth.models import User
from Core.models import Company

# Create your models here.
class Team(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_team')
    team_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    province = models.CharField(max_length=130, null=True, blank=True)
    country = models.CharField(max_length=56, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.team_name +"-   -"+ self.company.name