from rest_framework import serializers
from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        exclude = [
            'invoice',
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True)
    status_label = serializers.CharField(source='status.lookup_name', read_only=True)
    account_label = serializers.CharField(source='client.contact_id', read_only=True)

    class Meta:
        model = Invoice
        exclude = [
            'company',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        year = request.META.get('HTTP_YEAR')
        invoice_items = validated_data.pop('invoice_items')
        invoice = Invoice(company=request.company, creation_year=year, **validated_data)
        invoice.save()
        for item in invoice_items:
            invoice_item = InvoiceItem(invoice=invoice, **item)
            invoice_item.save()
        return invoice

    def update(self, instance, validated_data):
        if not instance.company.id == validated_data['company'].id:
            raise serializers.ValidationError({"message": "Invalid input."})
        InvoiceItem.objects.filter(invoice=instance).delete()
        invoice_items = validated_data.pop('invoice_items')
        validated_data['creation_year'] = instance.creation_year
        invoice = Invoice(pk=instance.id, **validated_data)
        invoice.save()
        for item in invoice_items:
            invoice_item = InvoiceItem(invoice=invoice, **item)
            invoice_item.save()
        return invoice


class InvoiceDeleteSerializer(serializers.ModelSerializer):
    invoices_list = serializers.ListField(required=True, child=serializers.IntegerField())

    class Meta:
        model = Invoice
        fields = ['invoices_list']
