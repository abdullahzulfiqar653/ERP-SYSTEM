from rest_framework import serializers
from .models import Contact

# ---------------------- Serializers for Contact Module ---------------------------#


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id',
            'contact_type',
            'name',
            'nif',
            'tax_address',
            'tax_postcode',
            'tax_province',
            'tax_country',
            'shipping_address',
            'shipping_postcode',
            'shipping_province',
            'shipping_country',
            'account_type',
            'vat',
            'ret_or_equiv',
            'payment_method',
            'payment_extension',
        ]


class ContactUpdateSerializer(serializers.ModelSerializer):
    nif = serializers.CharField(validators=[],)

    class Meta:
        model = Contact
        fields = [
            'contact_type',
            'name',
            'nif',
            'tax_address',
            'tax_postcode',
            'tax_province',
            'tax_country',
            'shipping_address',
            'shipping_postcode',
            'shipping_province',
            'shipping_country',
            'account_type',
            'vat',
            'ret_or_equiv',
            'payment_method',
            'payment_extension',
        ]


'''
serializer to accept list of company id's
'''


class ContactDeleteSerializer(serializers.ModelSerializer):
    contact_list = serializers.ListField(child=serializers.IntegerField(required=True))

    class Meta:
        model = Contact
        fields = [
            'contact_list'
        ]
