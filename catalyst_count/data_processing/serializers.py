from rest_framework import serializers
from .models import Company

class CompanyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
