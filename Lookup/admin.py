from django.contrib import admin
from .models import LookupName, LookupType, Tax, Payment_Day, AccountType


# Register your models here.
class TaxAdmin(admin.ModelAdmin):
    list_display = ['id', 'lookup_name', 'vat', 'ret', 'equiv', 'irfp']


class LookupNameAdmin(admin.ModelAdmin):
    search_fields = ['lookup_name']


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


admin.site.register(LookupName, LookupNameAdmin)
admin.site.register(LookupType)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Payment_Day)
admin.site.register(AccountType, AccountTypeAdmin)
