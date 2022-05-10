from django.contrib import admin
from .models import Expense, ExpenseItem, Purchase, PurchaseItem, Asset, AssetItem


# Register your models here.


class ExpenseItemAdmin(admin.TabularInline):
    model = ExpenseItem
    extra = 0


class ExpenseAdmin(admin.ModelAdmin):
    inlines = [ExpenseItemAdmin, ]
    list_display = ['id', 'company', 'invoice_date', 'due_date', 'creation_date']
    readonly_fields = ['creation_date', 'accounting_seat']


admin.site.register(Expense, ExpenseAdmin)


class PurchaseItemAdmin(admin.TabularInline):
    model = PurchaseItem
    extra = 0


class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseItemAdmin, ]
    list_display = ['id', 'company', 'invoice_date', 'due_date', 'creation_date']
    readonly_fields = ['creation_date', 'accounting_seat']


admin.site.register(Purchase, PurchaseAdmin)


class AssetItemAdmin(admin.TabularInline):
    model = AssetItem
    extra = 0


class AssetAdmin(admin.ModelAdmin):
    inlines = [AssetItemAdmin, ]
    list_display = ['id', 'company', 'invoice_date', 'due_date', 'creation_date']
    readonly_fields = ['creation_date', 'accounting_seat']


admin.site.register(Asset, AssetAdmin)
