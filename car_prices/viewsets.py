from django.db.models import Avg, F
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Brands, ModelInfo
from .serializers import BrandListSerializer, ModelInfoSerializer

@api_view(['GET', 'POST'])
def brands(request):
    '''
    GET /brands

    List all brands
    The average price of each brand is the average of its models average prices

    POST /brands

    You may add new brands. A brand name must be unique.
    If a brand name is already in use return a response code and error message reflecting it.

    '''
    if request.method == 'GET':
        data = Brands.objects.all().annotate(average_price=Avg(F('models__average_price')))

        serializer = BrandListSerializer(data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        name = request.data.get('name', '')
        if name:
            brand, created = Brands.objects.get_or_create(name=name)
            if created:
                return Response(request.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "brand already exists"}, status=status.HTTP_400_BAD_REQUEST)
        

            
        return Response({"error": "name is missing"}, status=status.HTTP_400_BAD_REQUEST)    
    
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['POST'])
def addModelToBrand(request, id):
    ''''
    POST /brands/:id/models

    You may add new models to a brand. A model name must be unique inside a brand.
    If the brand id doesn't exist return a response code and error message reflecting it.
    If the model name already exists for that brand return a response code and error message reflecting it.
    Average price is optional, if supply it must be greater than 100,000.
    '''
    name = request.data.get('name', '')
    avg_price = request.data.get('average_price', 0)
    if name:
        try:
            price = int(avg_price) if int(avg_price) > 100000 else 0
            if avg_price and price <= 100000:
                return Response({"error": "average price must be greater than 100000"}, status=status.HTTP_400_BAD_REQUEST)
            
            brand = Brands.objects.get(id=id)
            if ModelInfo.objects.filter(Q(brand_name=brand) & Q(name=name)).exists():
                return Response({"error": "model name already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            model = ModelInfo.objects.create(name=name, average_price=price, brand_name=brand)
            response = ModelInfoSerializer(model)
            return Response(response.data)
            
        except Brands.DoesNotExist:
            return Response({"error": "brand does not exists"}, status=status.HTTP_400_BAD_REQUEST) 

        
    return Response({"error": "name is missing"}, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['PUT'])
def editModels(request, id):
    '''
    PUT /models/:id

    You may edit the average price of a model.
    The average_price must be greater then 100,000.
    '''
    avg_price = request.data.get('average_price', 0)
    price = int(avg_price) if int(avg_price) > 100000 else 0
    
    if avg_price and price > 100000:
        try:
            model = ModelInfo.objects.get(id=id)
            model.average_price = price
            model.save()
            response = ModelInfoSerializer(model)
            return Response(response.data)
            
        except Brands.DoesNotExist:
            return Response({"error": "model does not exists"}, status=status.HTTP_400_BAD_REQUEST) 

    else:
        return Response({"error": "average price is missing or is less than 100000"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def listAllModels(request):
    '''
    GET /models?greater=&lower=

    List all models. 
    If greater param is included show all models with average_price greater than the param
    If lower param is included show all models with average_price lower than the param

    # /models?greater=380000&lower=400000
    '''
    greater_filter = request.query_params.get('greater', 0)
    lower_filter = request.query_params.get('lower', 0)
    
    if greater_filter or lower_filter:
        if (greater_filter):
            models = ModelInfo.objects.filter(Q(average_price__gt=greater_filter))
        if (lower_filter):
            models = ModelInfo.objects.filter(Q(average_price__lt=lower_filter))
        if (greater_filter and lower_filter):
            models = ModelInfo.objects.filter(Q(average_price__gt=greater_filter) & Q(average_price__lt=lower_filter))
        
        response = ModelInfoSerializer(models, many=True)
        return Response(response.data)
    
    else:
        models = ModelInfo.objects.all()
        response = ModelInfoSerializer(models, many=True)
        return Response(response.data)
