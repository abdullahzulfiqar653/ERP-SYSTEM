from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from Middleware.CustomMixin import CompanyPermissionsMixin
from Middleware.permissions import IsCompanyAccess
from .serializers import ExpenseSerializer, ExpenseDeleteSerializer
from .models import Expense
# from .filters import InvoiceFilter
from utils.pagination import LimitOffsetPagination


class ExpenseViewSet(ModelViewSet, CompanyPermissionsMixin):
    permission_classes = [permissions.IsAuthenticated, IsCompanyAccess]
    serializer_class = ExpenseSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = InvoiceFilter
    ordering_fields = ['id', ]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        year = self.request.META.get("HTTP_YEAR")
        return Expense.objects.filter(
            company=self.request.company, creation_year=year).order_by('-id')

    def delete(self, request):
        company = self.request.company
        serializer = ExpenseDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        Expense.objects.filter(pk__in=data['expenses_list'], company=company).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
