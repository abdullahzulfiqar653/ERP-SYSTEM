from django.db import models
from Core.models import Company
from Lookup.models import LookupName, Tax
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
# --------------------- team Models -------------------- #


class Team(models.Model):
    creation_date = models.DateField(auto_now_add=True, )
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
    creation_date = models.DateField(auto_now_add=True, )
    image = models.ImageField(
            blank=True, null=True, upload_to="employeeImages",
            default="employeeImages/image.jpg")
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
    nif = models.CharField(max_length=13,)
    social_security = models.TextField(null=True, blank=True)
    contract_type = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='contract_type_lookup_name', null=True)
    address = models.TextField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    province = models.CharField(max_length=130, null=True, blank=True)
    country = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='country_lookup_name', null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + "-   -" + self.name


def max_value_current_year(value):
    return MaxValueValidator(datetime.date.today().year)(value)


class PayRoll(models.Model):
    creation_date = models.DateField(auto_now_add=True, )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name='company_payroll')
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
    created_at_year = models.PositiveIntegerField(
        validators=[MinValueValidator(2020), max_value_current_year])
    created_at_month = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)])


class PayrollTeam(models.Model):
    payroll = models.ForeignKey(
        PayRoll, on_delete=models.CASCADE,
        related_name='teams_list')
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
