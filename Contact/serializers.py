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


class ContactListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    contact_type_label = serializers.CharField(source='contact_type.lookup_name')

    class Meta:
        model = Contact
        fields = [
            'id',
            'contact_id',
            'contact_type_label',
            'name',
            'nif',
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


class ContactListForExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'contact_id',
            'name',
            'account_type',
        ]


class ContactListForInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'contact_id',
            'name',
            'contact_type'
        ]


class ContactRetrieveForInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'contact_id',
            'name',
            'contact_type',
            'tax_address',
            'tax_postcode',
            'tax_province',
            'tax_country',
            'shipping_address',
            'shipping_postcode',
            'shipping_province',
            'shipping_country',
            'vat',
            'ret_or_equiv',
            'payment_method',
        ]
