from rest_framework import serializers
from .models import Expense, ExpenseItem
from .utils import get_expense_id


class ExpenseItemerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        exclude = [
            'expense',
        ]


class ExpenseSerializer(serializers.ModelSerializer):
    expense_items = ExpenseItemerializer(many=True)
    expense_accounting_seat = serializers.CharField(read_only=True)

    class Meta:
        model = Expense
        exclude = [
            'company',
            'creation_year',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        year = request.META.get('HTTP_YEAR')
        expense_items = validated_data.pop('expense_items')
        validated_data["expense_accounting_seat"] = get_expense_id()
        expense = Expense(company=request.company, creation_year=year, **validated_data)
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
        validated_data['creation_year'] = instance.creation_year
        validated_data['expense_accounting_seat'] = instance.expense_accounting_seat
        expense = Expense(pk=instance.id, company=company, **validated_data)
        expense.save()
        for item in expense_items:
            expense_items = ExpenseItem(expense=expense, **item)
            expense_items.save()
        return expense


class ExpenseDeleteSerializer(serializers.ModelSerializer):
    expenses_list = serializers.ListField(required=True, child=serializers.IntegerField())

    class Meta:
        model = Expense
        fields = ['expenses_list']
