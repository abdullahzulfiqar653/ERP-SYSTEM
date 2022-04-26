from .models import Expense, Purchase, Asset
import random


def get_expense_id():
    random_num = random.randint(470000000001, 479999999999)
    while Expense.objects.filter(expense_accounting_seat=random_num).exists():
        random_num = random.randint(470000000001, 479999999999)
    return random_num


def get_purchase_id():
    random_num = random.randint(480000000001, 489999999999)
    while Purchase.objects.filter(purchase_accounting_seat=random_num).exists():
        random_num = random.randint(480000000001, 489999999999)
    return random_num


def get_asset_id():
    random_num = random.randint(490000000001, 499999999999)
    while Asset.objects.filter(asset_accounting_seat=random_num).exists():
        random_num = random.randint(490000000001, 499999999999)
    return random_num
