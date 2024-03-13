from django.db.models import Avg, F

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Brands, ModelInfo
from .serializers import BrandListSerializer

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
