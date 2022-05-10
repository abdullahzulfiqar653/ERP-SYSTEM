from rest_framework import serializers
from .models import Expense, ExpenseItem, Purchase, PurchaseItem, Asset, AssetItem
from .utils import get_expense_id, get_purchase_id, get_asset_id


# --------------------Expense Serializers------------------ #
class ExpenseItemerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        exclude = [
            'expense',
        ]


class ExpenseSerializer(serializers.ModelSerializer):
    expense_items = ExpenseItemerializer(many=True)
    accounting_seat = serializers.CharField(read_only=True)

    class Meta:
        model = Expense
        exclude = [
            'company',
            'creation_date',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        # year = request.META.get('HTTP_YEAR')
        expense_items = validated_data.pop('expense_items')
        validated_data["accounting_seat"] = get_expense_id()
        expense = Expense(company=request.company, **validated_data)
        expense.save()
        for item in expense_items:
            expense_item = ExpenseItem(expense=expense, **item)
            expense_item.save()
        return expense

    def update(self, instance, validated_data):
        request = self.context.get('request')
        company = request.company
        if not instance.company.id == company.id:
            raise serializers.ValidationError({"message": "Invalid input."})
        ExpenseItem.objects.filter(expense=instance).delete()
        expense_items = validated_data.pop('expense_items')
        validated_data['creation_date'] = instance.creation_date
        validated_data['accounting_seat'] = instance.accounting_seat
        expense = Expense(pk=instance.id, company=company, **validated_data)
        expense.save()
        for item in expense_items:
            expense_items = ExpenseItem(expense=expense, **item)
            expense_items.save()
        return expense


class ExpenseDeleteSerializer(serializers.Serializer):
    expenses_list = serializers.ListField(required=True, child=serializers.IntegerField())


# --------------------Purchase Serializers------------------ #
class PurchaseItemerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        exclude = [
            'purchase',
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    purchase_items = PurchaseItemerializer(many=True)
    accounting_seat = serializers.CharField(read_only=True)

    class Meta:
        model = Purchase
        exclude = [
            'company',
            'creation_year',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        year = request.META.get('HTTP_YEAR')
        purchase_items = validated_data.pop('purchase_items')
        validated_data["accounting_seat"] = get_purchase_id()
        purchase = Purchase(company=request.company, creation_year=year, **validated_data)
        purchase.save()
        for item in purchase_items:
            purchase_item = PurchaseItem(purchase=purchase, **item)
            purchase_item.save()
        return purchase

    def update(self, instance, validated_data):
        request = self.context.get('request')
        company = request.company
        if not instance.company.id == company.id:
            raise serializers.ValidationError({"message": "Invalid input."})
        PurchaseItem.objects.filter(purchase=instance).delete()
        purchase_items = validated_data.pop('purchase_items')
        validated_data['creation_date'] = instance.creation_date
        validated_data['accounting_seat'] = instance.accounting_seat
        purchase = Purchase(pk=instance.id, company=company, **validated_data)
        purchase.save()
        for item in purchase_items:
            purchase_item = PurchaseItem(purchase=purchase, **item)
            purchase_item.save()
        return purchase


class PurchaseDeleteSerializer(serializers.Serializer):
    purchases_list = serializers.ListField(required=True, child=serializers.IntegerField())


# --------------------Asset Serializers------------------ #
class AssetItemerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetItem
        exclude = [
            'asset',
        ]


class AssetSerializer(serializers.ModelSerializer):
    asset_items = AssetItemerializer(many=True)
    accounting_seat = serializers.CharField(read_only=True)

    class Meta:
        model = Asset
        exclude = [
            'company',
            'creation_year',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        year = request.META.get('HTTP_YEAR')
        asset_items = validated_data.pop('asset_items')
        validated_data["accounting_seat"] = get_asset_id()
        asset = Asset(company=request.company, creation_year=year, **validated_data)
        asset.save()
        for item in asset_items:
            asset_item = AssetItem(asset=asset, **item)
            asset_item.save()
        return asset

    def update(self, instance, validated_data):
        request = self.context.get('request')
        company = request.company
        if not instance.company.id == company.id:
            raise serializers.ValidationError({"message": "Invalid input."})
        AssetItem.objects.filter(asset=instance).delete()
        asset_items = validated_data.pop('asset_items')
        validated_data['creation_date'] = instance.creation_date
        validated_data['accounting_seat'] = instance.accounting_seat
        asset = Asset(pk=instance.id, company=company, **validated_data)
        asset.save()
        for item in asset_items:
            asset_item = AssetItem(asset=asset, **item)
            asset_item.save()
        return asset


class AssetDeleteSerializer(serializers.Serializer):
    assets_list = serializers.ListField(required=True, child=serializers.IntegerField())
