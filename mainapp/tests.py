from django.test import TestCase
from django.test.client import Client


# Create your tests here.
from mainapp.models import ProductCategory, Product


class TestMainappCase(TestCase):

    EXPECTED_SUCCESS_CODE = 200
    def setUp(self):
        self.client = Client()


    def test_mainapp_urls(self):
        #главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        #
        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)