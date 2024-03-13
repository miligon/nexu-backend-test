from django.urls import path, include

from rest_framework import routers

from .viewsets import *

route = routers.SimpleRouter()

urlpatterns = route.urls + [
    path('brands', listAllBrands, name="list_brands"),
    path('brands/<int:id>/models', addModel, name="add_model_to_brand"),
]