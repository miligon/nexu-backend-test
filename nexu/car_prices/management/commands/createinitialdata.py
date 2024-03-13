import json
from django.core.management.base import BaseCommand
from django.db import transaction
from car_prices.models import Brands, ModelInfo

class Command(BaseCommand):
    help = 'Load models.json into database'

    @transaction.atomic
    def handle(self, *args, **options):
        print('Reading file ...')

        f = open('models.json', mode='r', encoding='utf8')
        data = json.load(f)
        for record in data:
            brand, created = Brands.objects.get_or_create(name=record['brand_name'])
            ModelInfo.objects.create(id=record['id'],
                                     brand_name=brand,
                                     name=record['name'],
                                     average_price=record['average_price'])
            print(record)
        
        print("Done!")