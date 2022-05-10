from django_filters import FilterSet
from .models import Expense, Purchase, Asset


class ExpenseFilter(FilterSet):
    class Meta:
        model = Expense
        fields = {
            "creation_date": ['gt', 'lt'],
            "accounting_seat": ["exact"],
            "invoice_date": ['exact'],
            "due_date": ['exact'],
        }


class PurchaseFilter(FilterSet):
    class Meta:
        model = Purchase
        fields = {
            "creation_date": ['gt', 'lt'],
            "accounting_seat": ["exact"],
            "invoice_date": ['exact'],
            "due_date": ['exact'],
        }


class AssetFilter(FilterSet):
    class Meta:
        model = Asset
        fields = {
            "creation_date": ['gt', 'lt'],
            "accounting_seat": ["exact"],
            "invoice_date": ['exact'],
            "due_date": ['exact'],
        }
