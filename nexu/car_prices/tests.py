from django.urls import reverse
from django.db.models import Avg, F, Q
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Brands, ModelInfo


class Tests(APITestCase):
    def setUp(self):
        brand = Brands.objects.create(id=1, name="Acura")
        ModelInfo.objects.create(id=1, name='test1', average_price=100000, brand_name=brand)
        ModelInfo.objects.create(id=2, name='test2', average_price=300000, brand_name=brand)
        ModelInfo.objects.create(id=3, name='test3', average_price=600000, brand_name=brand)
        ModelInfo.objects.create(id=4, name='test4', average_price=1000000, brand_name=brand)
    
    def test_list_brands(self):
        """
        Test list brands endpoint
        """
        url = reverse('brands')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = ModelInfo.objects.filter(brand_name=1).aggregate(avg_price=Avg(F('average_price')))
        self.assertEqual(response.json()[0]['average_price'], data['avg_price'])

    def test_add_brands(self):
        """
        Test add brands endpoint
        """
        url = reverse('brands')
        data = {"name": "Toyota"}
        response = self.client.post(url, data, format='json')
        
        self.assertTrue(Brands.objects.filter(name='Toyota').exists())

        data = {"name": "Toyota"}
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_models_to_brands(self):
        """
        Test add models to brands endpoint
        """
        url = reverse('add_model_to_brand', kwargs={'id':1})
        data = {"name": "test5", "average_price": 406400}
        response = self.client.post(url, data, format='json')
        
        self.assertTrue(ModelInfo.objects.filter(Q(brand_name=1) & Q(name="test5")).exists())

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('add_model_to_brand', kwargs={'id':2})
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_model(self):
        """
        Test edit avg price of model
        """
        url = reverse('edit_model', kwargs={'id':1})
        data = {"average_price": 321654}
        response = self.client.put(url, data, format='json')

        model = ModelInfo.objects.get(id=1)
        
        self.assertEqual(model.average_price, 321654)

        url = reverse('edit_model', kwargs={'id':1})
        data = {"average_price": 120}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
