from django.contrib import admin
from .models import Invoice, InvoiceItem


# Register your models here.


class InvoiceItemAdmin(admin.TabularInline):
    model = InvoiceItem
    extra = 0


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemAdmin, ]
    list_display = ['id', 'company', 'invoice_date', 'due_date', 'creation_year', 'status']


admin.site.register(Invoice, InvoiceAdmin)
