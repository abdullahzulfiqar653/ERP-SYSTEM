from django.db import models

# Create your models here.
# ------------------------------Look Up Classes----------------------------- #


class LookupType(models.Model):
    lookup_type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.lookup_type


class LookupName(models.Model):
    lookup_type = models.ForeignKey(
        LookupType, on_delete=models.CASCADE,
        related_name='lookupTypeName')
    lookup_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.lookup_name


class Tax(models.Model):  # Ret is a tax type like VAT
    lookup_name = models.ForeignKey(
        LookupName, on_delete=models.CASCADE,
        related_name='lookupName')
    ret = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    equiv = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    vat = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    irfp = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.id)


class AccountType(models.Model):  # This relate to chart of account.
    lookup_name = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='account_type_lookup_name', null=True, blank=True)
    account_number = models.CharField(max_length=12, unique=True)
    english_name = models.CharField(max_length=256,)
    chart = models.CharField(max_length=128,)
    category = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='account_category_lookup_name', null=True)
    financial_statement = models.CharField(max_length=128, )

    def __str__(self):
        return str(self.english_name)


class PaymentDay(models.Model):  # This relate to chart of account.
    lookup_name = models.ForeignKey(
        LookupName, on_delete=models.CASCADE,
        related_name='payment_day_lookup_name')
    name = models.CharField(max_length=256, unique=True)
    day = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.name)
