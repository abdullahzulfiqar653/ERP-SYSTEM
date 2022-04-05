from django.db import models
from Core.models import Company

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
        return str(self.lookup_type) + " - " + self.lookup_name


class Tax(models.Model):  # Ret is a tax type like VAT
    lookup_name = models.ForeignKey(
        LookupName, on_delete=models.CASCADE,
        related_name='lookupName')
    ret = models.DecimalField(max_digits=5, decimal_places=3, default=0.0)
    equiv = models.DecimalField(max_digits=5, decimal_places=3, default=0.0)
    vat = models.DecimalField(max_digits=5, decimal_places=3, default=0.0)
    irfp = models.DecimalField(max_digits=5, decimal_places=3, default=0.0)

    def __str__(self):
        return str(self.id)


class AccountType(models.Model):  # This relate to chart of account.
    lookup_name = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='account_type_lookup_name', null=True)
    account_number = models.CharField(max_length=12, unique=True)
    english_name = models.CharField(max_length=256, unique=True)
    chart = models.CharField(max_length=128,)
    category = models.ForeignKey(
        LookupName, on_delete=models.SET_NULL,
        related_name='account_category_lookup_name', null=True)
    financial_statement = models.CharField(max_length=128, )

    def __str__(self):
        return str(self.english_name)


class Payment_Day(models.Model):  # This relate to chart of account.
    lookup_type = models.ForeignKey(
        LookupType, on_delete=models.CASCADE,
        related_name='payment_day_lookup_type')
    name = models.CharField(max_length=256, unique=True)
    day = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.name)


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
