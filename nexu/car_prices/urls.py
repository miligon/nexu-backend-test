from django.urls import path, include

from rest_framework import routers

from .viewsets import *

route = routers.SimpleRouter()

urlpatterns = route.urls + [
    path('brands', listAllBrands, name="list_brands"),
]