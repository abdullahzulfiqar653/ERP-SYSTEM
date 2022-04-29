import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from Contact.models import Contact
from Lookup.models import LookupName, Tax
from Core.models import Company
# Create your models here.


def max_value_current_year(value):
    return MaxValueValidator(datetime.date.today().year)(value)


class Invoice(models.Model):
    creation_year = models.PositiveIntegerField(
        validators=[MinValueValidator(2020), max_value_current_year], blank=True, null=True)
    status = models.CharField(max_length=50, default="Pending")
    # status = models.ForeignKey(
    #     LookupName, on_delete=models.SET_NULL,
    #     related_name='invoice_status', null=True, )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name='company_invoice')
    invoice_date = models.DateField()
    client = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='invoiceContactItems')
    base_amount = models.DecimalField(max_digits=10, decimal_places=2,)
    vat_percentage = models.ForeignKey(
        Tax, on_delete=models.SET_NULL,
        related_name='invoice_vat_tax', null=True)
    vat_total = models.DecimalField(max_digits=8, decimal_places=2, )
    equiv_percentage = models.ForeignKey(
        Tax, on_delete=models.SET_NULL,
        related_name='invoice_ret_tax', null=True)
    equiv_total = models.DecimalField(max_digits=8, decimal_places=2, )
    total = models.DecimalField(max_digits=10, decimal_places=2, )
    payment_method = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='invoice_payment_method_name', null=True, )
    due_date = models.DateField(auto_now_add=False)
    iban = models.CharField(max_length=34, blank=True, null=True)

    tax_address = models.TextField(blank=True, null=True)
    tax_postcode = models.CharField(max_length=10, blank=True, null=True)
    tax_province = models.CharField(max_length=130, blank=True, null=True)
    tax_country = models.ForeignKey(
        LookupName, on_delete=models.PROTECT,
        related_name='invoice_tax_country_name',)

    shipping_address = models.TextField(blank=True, null=True)
    shipping_postcode = models.CharField(max_length=10, blank=True, null=True)
    shipping_province = models.CharField(max_length=130, blank=True, null=True)
    shipping_country = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='invoice_shipping_country_name', null=True)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_items')
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2,)
    discount = models.DecimalField(max_digits=8, decimal_places=2,)
    base = models.DecimalField(max_digits=8, decimal_places=2, )
