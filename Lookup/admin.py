from django.contrib import admin
from .models import LookupName, LookupType, Tax, Payment_Day, AccountType


# Register your models here.
class TaxAdmin(admin.ModelAdmin):
    list_display = ['id', 'lookup_name', 'vat', 'ret', 'equiv', 'irfp']


admin.site.register(LookupName)
admin.site.register(LookupType)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Payment_Day)
admin.site.register(AccountType)
