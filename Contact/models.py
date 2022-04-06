from django.db import models
from Lookup.models import LookupName, AccountType, Tax, Payment_Day
from Core.models import Company
# Create your models here.


class Contact(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name='company_contact')
    contact_type = models.ForeignKey(
        LookupName, on_delete=models.CASCADE,
        related_name='contact_type_lookup_name')  # option field
    name = models.CharField(max_length=255)
    # auto fill according to the type of account_type in PaymentSection
    contact_id = models.CharField(max_length=12)
    nif = models.CharField(max_length=13, unique=True)
    # Client address of tax
    tax_address = models.TextField()
    tax_postcode = models.CharField(max_length=10,)
    tax_province = models.CharField(max_length=130,)
    tax_country = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='tax_country_name', null=True)  # option fields
    # Client Address for shipping
    shipping_address = models.TextField()
    shipping_postcode = models.CharField(max_length=10,)
    shipping_province = models.CharField(max_length=130,)
    shipping_country = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='shipping_country_name', null=True)  # option field
    #  chart of account type
    account_type = models.ForeignKey(
        AccountType, on_delete=models.SET_NULL,
        related_name='account_type_name', null=True)  # option field
    vat = models.ForeignKey(
        Tax, on_delete=models.SET_NULL,
        related_name='vat_tax', null=True)  # option field
    # option field
    ret_or_equiv = models.ForeignKey(
        Tax, on_delete=models.SET_NULL,
        related_name='ret_or_re_tax', null=True)
    payment_method = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='payment_method_name', null=True)
    payment_extension = models.ForeignKey(
        Payment_Day, on_delete=models.SET_NULL,
        related_name='payment_extension_days', null=True)  # option field
