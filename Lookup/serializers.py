from rest_framework import serializers
from .models import LookupType, LookupName, Tax


# ---------------------- Serializers for Lookups Module ---------------------------#


class LookupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookupType
        fields = ['lookup_type']


class LookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookupName
        fields = [
            'id',
            'lookup_name',
        ]


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        exclude = ['lookup_name', ]
