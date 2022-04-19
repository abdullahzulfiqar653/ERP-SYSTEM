from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions, status
from Middleware.CustomMixin import CompanyPermissionsMixin
from Middleware.permissions import IsCompanyAccess
from .serializers import InvoiceSerializer, InvoiceDeleteSerializer
from .models import Invoice


class InoviceViewSet(ModelViewSet, CompanyPermissionsMixin):
    permission_classes = [permissions.IsAuthenticated, IsCompanyAccess]
    serializer_class = InvoiceSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Invoice.objects.filter(company=self.request.company).order_by('-id')

    def perform_update(self, serializer):
        serializer.validated_data['company'] = self.request.company
        return super().perform_update(serializer)

    def delete(self, request):
        company = self.request.company
        serializer = InvoiceDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        Invoice.objects.filter(pk__in=data['invoices_list'], company=company).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
