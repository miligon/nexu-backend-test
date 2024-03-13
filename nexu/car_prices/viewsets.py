from django.db.models import Avg

from rest_framework.decorators import api_view

from .models import ModelInfo

@api_view(['GET'])
def listAllbrands(request):
    return 'hola'