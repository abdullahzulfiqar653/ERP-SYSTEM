from .models import LookupName, Tax, LookupType
from rest_framework import generics
from rest_framework import permissions
from .serializers import (
    LookupTypeSerializer,
    LookupSerializer,
    TaxSerializer,
)

# Create your views here.
# ---------------------- Views for Lookups Module ---------------------------------#


class LookupTypeListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LookupTypeSerializer
    queryset = LookupType.objects.all()


class LookupListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LookupSerializer

    def get_queryset(self):
        return LookupName.objects.filter(lookup_type__lookup_type=self.kwargs['lookup'])


class TaxListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TaxSerializer

    def get_queryset(self):
        if "client" == self.kwargs['lookup'].lower() or "debitor" == self.kwargs['lookup'].lower():
            return Tax.objects.filter(lookup_name__lookup_name=self.kwargs['lookup'].lower()).values('id', 'vat', 'equiv')
        if "provider" == self.kwargs['lookup'].lower() or "creditor" == self.kwargs['lookup'].lower():
            return Tax.objects.filter(lookup_name__lookup_name=self.kwargs['lookup'].lower()).values('id', 'vat', 'ret')
        if "payrolltax" == self.kwargs['lookup'].lower():
            return Tax.objects.filter(lookup_name__lookup_name=self.kwargs['lookup'].lower()).values('id', 'irfp')
        return Tax.objects.none()
