from django.urls import path, include

from rest_framework import routers

from .viewsets import *

route = routers.SimpleRouter()

urlpatterns = route.urls + [
    path('brands', listAllBrands, name="list_brands"),
    path('brands/<int:id>/models', addModelToBrand, name="add_model_to_brand"),
    path('models/<int:id>', editModels, name="edit_model"),
    path('models', listAllModels, name="list_models"),
]