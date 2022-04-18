from .models import Contact
from django_filters import FilterSet


class ContactFilter(FilterSet):
    class Meta:
        model = Contact
        fields = {
            "contact_type__id": ['exact'],
            "name": ['iexact'],
            # "contact_id": ['exact'],
            "nif": ['exact'],

            # "tax_address": ['icontains'],
            # "tax_postcode": ['exact'],
            # "tax_province": ['iexact'],
            # "tax_country__lookup_name": ['iexact'],

            # "shipping_address": ['icontains'],
            # "shipping_postcode": ['exact'],
            # "shipping_province": ['iexact'],
            # "shipping_country__lookup_name": ['iexact'],

            # "account_type__english_name": ['iexact'],
            # "vat": ['exact'],
            # "ret_or_equiv": ['exact'],
            # "payment_method__lookup_name": ['iexact'],
            # "payment_extension__day": ['iexact'],
        }
