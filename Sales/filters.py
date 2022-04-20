from django_filters import FilterSet
from .models import Invoice


class InvoiceFilter(FilterSet):
    class Meta:
        model = Invoice
        fields = {
            "due_date": ['exact'],
            "total": ['gt', 'lt'],
            "status__id": ["exact"],
        }
