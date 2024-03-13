from django.db.models import Avg, F
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Brands, ModelInfo
from .serializers import BrandListSerializer, ModelInfoSerializer

@api_view(['GET', 'POST'])
def listAllBrands(request):
    if request.method == 'GET':
        data = Brands.objects.all().annotate(average_price=Avg(F('models__average_price')))

        serializer = BrandListSerializer(data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        name = request.data.get('name', '')
        if name:
            brand, created = Brands.objects.get_or_create(name=name)
            if created:
                return Response(request.data)
            else:
                return Response({"error": "brand already exists"})
        

            
        return Response({"error": "name is missing"})    
    
    return Response({"error": "Method not allowed"})
    
@api_view(['POST'])
def addModel(request, id):
    name = request.data.get('name', '')
    avg_price = request.data.get('average_price', 0)
    if name:
        try:
            price = int(avg_price) if int(avg_price) > 100000 else 0
            if avg_price and price <= 100000:
                return Response({"error": "average price must be greater than 100000"})
            
            brand = Brands.objects.get(id=id)
            if ModelInfo.objects.filter(Q(brand_name=brand) & Q(name=name)).exists():
                return Response({"error": "model name already exists"})
            
            model = ModelInfo.objects.create(name=name, average_price=price, brand_name=brand)
            response = ModelInfoSerializer(model)
            return Response(response.data)
            
        except Brands.DoesNotExist:
            return Response({"error": "brand does not exists"}) 

        
    return Response({"error": "name is missing"})  