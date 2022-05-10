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
    client_id = serializers.CharField(source='client.contact_id', read_only=True)
    client_label = serializers.CharField(source='client.name', read_only=True)
    payment_method_label = serializers.CharField(source='payment_method.lookup_name', read_only=True)
    status = serializers.CharField(read_only=True)
    vat_percentage_label = serializers.CharField(source='vat_percentage.vat', read_only=True)
    equiv_percentage_label = serializers.CharField(source='equiv_percentage.equiv', read_only=True)

    class Meta:
        model = Invoice
        exclude = [
            'company',
            'creation_date',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        invoice_items = validated_data.pop('invoice_items')
        invoice = Invoice(company=request.company, **validated_data)
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
