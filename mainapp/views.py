import random

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import json, os, django

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory, Locations

def get_hot_product():
    product_list = Product.objects.filter(category__is_active=True, is_active=True).select_related('category')
    return random.sample(list(product_list), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category_id=hot_product.category_id, is_active=True, category__is_active=True).exclude(pk=hot_product.pk).select_related('category')[:3]
    return same_products


def main(request):
    products_list = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:4]
    content = {
        'title': 'главная',
        'products': products_list,
    }
    return render(request, 'mainapp/index.html', content)


def contact(request):
    locations = Locations.objects.all()
    content = {
        'title' : 'контакты',
        'locations' : locations,
    }
    return render(request, 'mainapp/contact.html', content)


def products(request, category_pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)

    if category_pk is not None:
        if category_pk == 0:
            products_items = Product.objects.filter(is_active=True, category__is_active=True)
            category = {'pk': '0', 'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=category_pk)
            products_items = Product.objects.filter(category=category, is_active=True, category__is_active=True).select_related('category').order_by('-price')

        paginator = Paginator(products_items, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title' : title,
        'links_menu' : links_menu,
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
        'links_menu': ProductCategory.objects.all(),
        'same_products': get_same_products(product_item)
    }

    return render(request,'mainapp/product.html', content)