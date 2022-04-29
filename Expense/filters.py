# from django_filters import FilterSet
# from .models import Purchase, Expense


# class ExpenseFilter(FilterSet):
#     class Meta:
#         model = Expense
#         fields = {
#             "expense_accounting_seat": ["exact"],
#             "name": ['icontains'],
#             "surname": ['icontains'],
#             "contract_type": ['exact'],
#             "enddate": ['exact'],
#             "team": ["exact"],
#             "current_salary": ['gt', 'lt'],
#         }


# class PurchaseFilter(FilterSet):
#     class Meta:
#         model = Purchase
#         fields = {
#             "team_name": ['icontains'],
#             "address": ['icontains'],
#             "postcode": ['exact'],
#             "province": ['iexact'],
#             "country__id": ['exact'],
#             "note": ['icontains'],
#         }


# class PayRollFilter(FilterSet):
#     class Meta:
#         model = PayRoll
#         fields = {
#             "id": ["exact"],
#             "created_at_year": ["exact"],
#             "created_at_month": ["exact"],
#             "gross": ['gt', 'lt'],
#             "bonus": ['gt', 'lt'],
#             "total_gross": ['gt', 'lt'],
#             "irfp": ['gt', 'lt'],
#             "irfp_total": ['gt', 'lt'],
#             "ss_employee": ['gt', 'lt'],
#             "net": ['gt', 'lt'],
#             "ss_company": ['gt', 'lt'],
#             "discount": ['gt', 'lt'],
#             "company_cost": ['gt', 'lt']
#         }
