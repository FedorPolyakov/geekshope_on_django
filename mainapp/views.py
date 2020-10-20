import random

from django.conf import settings
from django.shortcuts import render, get_object_or_404
import json, os, django

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory, Locations

def get_hot_product():
    product_list = Product.objects.all().exclude(category__is_active=False).exclude(is_active=False)
    return random.sample(list(product_list), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category_id=hot_product.category_id).exclude(pk=hot_product.pk).exclude(is_active=False)[:3]
    return same_products

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []

def main(request):
    products_list = Product.objects.all().exclude(is_active=False)[:4]
    content = {
        'title': 'главная',
        'products': products_list,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', content)

def contact(request):
    locations = Locations.objects.all()
    content = {
        'title' : 'контакты',
        'locations' : locations,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contact.html', content)


def products(request, category_pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all().exclude(is_active=False)

    if category_pk is not None:
        if category_pk == 0:
            products_items = Product.objects.all().exclude(is_active=False)
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=category_pk)
            products_items = Product.objects.filter(category=category).order_by('-price').exclude(is_active=False)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_items,
            'basket': get_basket(request.user),
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title' : title,
        'links_menu' : links_menu,
        'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', content)

  
def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    title = product_item.name
    content = {
        'title': title,
        'product': product_item,
        'basket': get_basket(request.user),
        'links_menu': ProductCategory.objects.all(),
        'same_products': get_same_products(product_item)
    }

    return render(request,'mainapp/product.html', content)
#old code
# image_src = "product-1.jpg"
# image_href = "/product/2/"
# with open(os.path.join(settings.BASE_DIR, 'mainapp/json_files/links_menu.json'), encoding='UTF-8') as json_file:
#     json_data = json_file.read()
#     links_menu = json.loads(json_data)
# with open(os.path.join(settings.BASE_DIR, 'mainapp/json_files/tab_contents.json'), encoding='UTF-8') as json_file:
#     json_data = json_file.read()
#     tab_contents = json.loads(json_data)
# with open(os.path.join(settings.BASE_DIR, 'mainapp/json/contact_locations.json'), encoding='UTF-8') as json_file:
#     json_data = json_file.read()
#     locations = json.loads(json_data)

