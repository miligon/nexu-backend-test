from rest_framework import serializers

from .models import *

class ModelInfoBulkCreateSerializer(serializers.ListSerializer):  
        def create(self, validated_data): 
            partidas = [ModelInfo(**item) for item in validated_data]  
            return ModelInfo.objects.bulk_create(partidas)
        
class ModelInfoSerializer(serializers.ModelSerializer):
    nombre = models.CharField(ource='name')
    class Meta:
        model = ModelInfo
        fields = ('id',
                  'nombre',
                  'average_price')
        list_serializer_class = ModelInfoBulkCreateSerializer