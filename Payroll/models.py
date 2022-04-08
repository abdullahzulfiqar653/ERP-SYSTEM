from django.db import models
from Core.models import Company
from Lookup.models import LookupName, Tax
# Create your models here.
# --------------------- team Models -------------------- #


class Team(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name='company_team')
    team_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    province = models.CharField(max_length=130, null=True, blank=True)
    country = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='team_country_lookup_name', null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.team_name + "-   -" + self.company.name


# --------------------- Employee Models -------------------- #


class Employee(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name='company_employee')
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    # spain tax number
    nif = models.CharField(max_length=13, null=True, blank=True, unique=True)
    social_security = models.TextField(null=True, blank=True)
    contract_type = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='contract_type_lookup_name', null=True)
    address = models.TextField(null=True, blank=True)
    enddate = models.DateField()
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    province = models.CharField(max_length=130, null=True, blank=True)
    country = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='country_lookup_name', null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + "-   -" + self.name


class PayRoll(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name='company_payroll')
    created_at = models.DateField(auto_now_add=False)
    gross = models.DecimalField(max_digits=12, decimal_places=2, )
    bonus = models.DecimalField(max_digits=12, decimal_places=2, )
    total_gross = models.DecimalField(max_digits=12, decimal_places=2, )
    irfp = models.DecimalField(max_digits=5, decimal_places=2, )  # total percent applied on all employees
    irfp_total = models.DecimalField(max_digits=12, decimal_places=2, )  # irfp total amount
    ss_employee = models.DecimalField(max_digits=10, decimal_places=2, )  # need to ask
    net = models.DecimalField(max_digits=12, decimal_places=2, )
    ss_company = models.DecimalField(max_digits=12, decimal_places=2, )
    discount = models.DecimalField(max_digits=12, decimal_places=2, )
    company_cost = models.DecimalField(max_digits=12, decimal_places=2, )


class PayrollTeam(models.Model):
    payroll = models.ForeignKey(
        PayRoll, on_delete=models.CASCADE,
        related_name='payroll_teams')
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True, blank=True)


class PayRollItem(models.Model):
    payroll = models.ForeignKey(
        PayRoll, on_delete=models.CASCADE,
        related_name='payroll_items')
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL,
        related_name='employee_payroll', null=True)
    gross = models.DecimalField(max_digits=10, decimal_places=2, )
    bonus = models.DecimalField(max_digits=10, decimal_places=2, )
    total_gross = models.DecimalField(max_digits=10, decimal_places=2, )
    irfp = models.ForeignKey(  # A tax type in percentage
        Tax, on_delete=models.SET_NULL,
        related_name='irfp_tax', null=True)
    irfp_total = models.DecimalField(max_digits=10, decimal_places=2, )  # Value of irft
    ss_employee = models.DecimalField(max_digits=10, decimal_places=2, )  # A calculated tax
    net = models.DecimalField(max_digits=10, decimal_places=2, )
    ss_company = models.DecimalField(max_digits=10, decimal_places=2, )
    discount = models.DecimalField(max_digits=10, decimal_places=2, )
    company_cost = models.DecimalField(max_digits=10, decimal_places=2, )
