from django.contrib import admin
from .models import LookupName, LookupType, Tax, PaymentDay, AccountType


# Register your models here.
class TaxAdmin(admin.ModelAdmin):
    list_display = ['id', 'lookup_name', 'vat', 'ret', 'equiv', 'irfp']


class LookupNameAdmin(admin.ModelAdmin):
    search_fields = ['lookup_name']
    list_display = ['lookup_type', 'lookup_name']


class AccountTypeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['lookup_name', 'category']
    list_display = [
        'lookup_name',
        'account_number',
        'chart',
        'category',
        'financial_statement'
    ]
    search_fields = ['lookup_name__lookup_name']


class PaymentDayAdmin(admin.ModelAdmin):
    autocomplete_fields = ['lookup_name']
    list_display = [
        'lookup_name',
        'name',
        'day',
    ]


admin.site.register(LookupName, LookupNameAdmin)
admin.site.register(LookupType)
admin.site.register(Tax, TaxAdmin)
admin.site.register(PaymentDay, PaymentDayAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
