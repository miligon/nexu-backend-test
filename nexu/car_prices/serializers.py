from rest_framework import serializers

from .models import *

class BrandListSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='name')
    average_price = serializers.IntegerField()

    class Meta:
        model = Brands
        fields = ('id',
                  'nombre',
                  'average_price'
                  )

class ModelInfoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='name')
    class Meta:
        model = ModelInfo
        fields = ('id',
                  'name',
                  'average_price')