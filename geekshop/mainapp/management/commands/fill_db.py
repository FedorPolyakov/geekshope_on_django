import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, Locations

FILE_PATH = os.path.join(settings.BASE_DIR, 'mainapp/json')

def load_from_json(file_name):
    with open(os.path.join(FILE_PATH, file_name + ".json"), 'r', errors='ignore', encoding='UTF-8') as json_file:
        return json.load(json_file)

class Command(BaseCommand):

    def handle(self, *args, **options):

        categories = load_from_json("categories")
        ProductCategory.objects.all().delete()
        for cat in categories:
            ProductCategory.objects.create(**cat)
            # new_cat = ProductCategory(**cat)
            # new_cat.save()

        products = load_from_json("products")
        Product.objects.all().delete()
        for product in products:
            cat_name = product['category']
            _cat = ProductCategory.objects.get(name=cat_name)
            product['category'] = _cat
            Product.objects.create(**product)

        locations = load_from_json("contact__locations")
        Locations.objects.all().delete()
        for location in locations:
            Locations.objects.create(**location)


        ShopUser.objects.create_superuser(username='django', password='geekbrains', age=30)