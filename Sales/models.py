from django.db import models
from Contact.models import Contact
from Lookup.models import AccountType, LookupName
from Core.models import Company
# Create your models here.


class Invoice(models.Model):
    creation_date = models.DateField()
    status = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='invoice_status', null=True, )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name='company_invoice')
    invoice_date = models.DateField()
    client = models.ForeignKey(Contact, on_delete=models.PROTECT)
    account = models.ForeignKey(
        AccountType, on_delete=models.PROTECT,
        related_name='invoice_account_type_name')
    base_amount = models.DecimalField(max_digits=10, decimal_places=2,)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, )
    vat_total = models.DecimalField(max_digits=8, decimal_places=2, )
    ret_percentage = models.DecimalField(max_digits=5, decimal_places=2, )
    ret_total = models.DecimalField(max_digits=8, decimal_places=2, )
    total = models.DecimalField(max_digits=10, decimal_places=2, )
    payment_method = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='invoice_payment_method_name', null=True, )
    due_date = models.DateField(auto_now_add=False)
    iban = models.CharField(max_length=34)

    tax_address = models.TextField()
    tax_postcode = models.CharField(max_length=10,)
    tax_province = models.CharField(max_length=130,)
    tax_country = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='invoice_tax_country_name', null=True)

    shipping_address = models.TextField()
    shipping_postcode = models.CharField(max_length=10,)
    shipping_province = models.CharField(max_length=130,)
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
