from django.contrib import admin
from .models import Expense, ExpenseItem


# Register your models here.


class ExpenseItemAdmin(admin.TabularInline):
    model = ExpenseItem
    extra = 0


class ExpenseAdmin(admin.ModelAdmin):
    inlines = [ExpenseItemAdmin, ]
    list_display = ['id', 'company', 'invoice_date', 'due_date', 'creation_year']
    readonly_fields = ['creation_year', 'expense_accounting_seat']


admin.site.register(Expense, ExpenseAdmin)
