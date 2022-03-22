
from os import pardir
from socket import NI_NOFQDN
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

class ContractTypeEnum(models.IntegerChoices):
    PERMANENT = 1, 'permanent'
    CONTRACT = 2, 'contract'
    TRAINING = 3, 'training'

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_employee')
    team = models.OneToOneField(Team, on_delete=models.SET_NULL,  null=True, blank=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    nif = models.CharField(max_length=13, null=True, blank=True, unique=True)
    social_security = models.TextField(null=True, blank=True)
    contract_type = models.SmallIntegerField(choices=ContractTypeEnum.choices)
    address = models.TextField(null=True, blank=True)
    enddate = models.DateField()
    current_salary = models.DecimalField(max_digits=8, decimal_places=2)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    province = models.CharField(max_length=130, null=True, blank=True)
    country = models.CharField(max_length=56, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

class PayRoll(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_payroll')
    created_at = models.DateField(auto_now_add=False)

class PayRollItem(models.Model):
    payroll = models.ForeignKey(PayRoll, on_delete=models.CASCADE, related_name='company_payroll')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_payroll')
    gross = models.DecimalField(max_digits=10, decimal_places=2, )
    bonus = models.DecimalField(max_digits=10, decimal_places=2, )
    total_gross = models.DecimalField(max_digits=10, decimal_places=2,)
    

class Contact(models.Model):
    type = models.CharField(max_length=55) #option field
    name = models.CharField(max_length=255)
    account_id = models.CharField(max_length=12) #auto fill according to the type of account_type in PaymentSection
    nif = models.CharField(max_length=13, null=True, blank=True, unique=True)


class ContactTaxAddress(models.Model):
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='contact_taxAddress')
    address = models.TextField()
    postcode = models.CharField(max_length=10, null=True, blank=True)
    province = models.CharField(max_length=130, null=True, blank=True)
    country = models.CharField(max_length=56, null=True, blank=True) #option fields


class ContactShipAddress(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_shipAddress')
    address = models.TextField()
    postcode = models.CharField(max_length=10, null=True, blank=True)
    province = models.CharField(max_length=130, null=True, blank=True)
    country = models.CharField(max_length=56, null=True, blank=True) #option field


class ContactPayment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_payment')
    account_type = models.CharField(max_length=55) #option field
    vat = models.IntegerField() #option field
    ret_or_re = models.CharField(max_length=55) #option field
    payment_method = models.CharField(max_length=55) #option field
    date = models.DateField()