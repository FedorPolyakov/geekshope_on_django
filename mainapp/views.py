from django.conf import settings
from django.shortcuts import render, get_object_or_404
import json, os, django

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory, Locations

def main(request):
    products_list = Product.objects.all()[:4]
    content = {
        'title': 'главная',
        # 'tabs'  : tab_contents,
        'products': products_list,
    }
    return render(request, 'mainapp/index.html', content)


def contact(request):
    locations = Locations.objects.all()
    content = {
        'title' : 'контакты',
        'locations' : locations
    }
    return render(request, 'mainapp/contact.html', content)


def products(request, category_pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    basket = Basket.objects.filter(user=request.user) #то что надо
    basket_q = sum(list(Basket.objects.filter(user_id=1).values_list('quantity', flat=True)))
    basket_prod_id = list(Basket.objects.filter(user=request.user).values_list('product_id', flat=True))
    product_prices_all = sum(list(Product.objects.filter(id__in=basket_prod_id).values_list('price', flat=True)))
    total_price = int(basket_q)*int(product_prices_all)


    if category_pk is not None:
        if category_pk == 0:
            products_items = Product.objects.all()
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=category_pk)
            products_items = Product.objects.filter(category=category).order_by('-price')

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_items,
            'basket': basket,
            'basket_q': basket_q,
            'total_price': total_price,
        }
        return render(request, 'mainapp/products_list.html', content)

    content = {
        'title' : title,
        'links_menu' : links_menu,
        'basket': basket,
        'basket_q': basket_q,
        'total_price': total_price,
    }
    return render(request, 'mainapp/products.html', content)

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