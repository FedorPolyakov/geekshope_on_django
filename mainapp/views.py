from django.conf import settings
from django.shortcuts import render
import json, os, django
from mainapp.models import Product, ProductCategory

# image_src = "product-1.jpg"
# image_href = "/product/2/"


def main(request):
    # with open(os.path.join(settings.BASE_DIR, 'mainapp/json_files/tab_contents.json'), encoding='UTF-8') as json_file:
    #     json_data = json_file.read()
    #     tab_contents = json.loads(json_data)

    products_list = Product.objects.all()[:4]
    content = {
        'title': 'главная',
        # 'tabs'  : tab_contents,
        'products': products_list,
    }
    return render(request, 'mainapp/index.html', content)

def contact(request):
    with open(os.path.join(settings.BASE_DIR, 'mainapp/json_files/locations.json'), encoding='UTF-8') as json_file:
        json_data = json_file.read()
        locations = json.loads(json_data)

    content = {
        'title' : 'контакты',
        'locations' : locations
    }
    return render(request, 'mainapp/contact.html', content)

def products(request, category_pk=None):
    print(category_pk)
    # with open(os.path.join(settings.BASE_DIR, 'mainapp/json_files/links_menu.json'), encoding='UTF-8') as json_file:
    #     json_data = json_file.read()
    #     links_menu = json.loads(json_data)
    links_menu = ProductCategory.objects.all()
    content = {
        'title' : 'продукты',
        'links_menu' : links_menu
    }
    return render(request, 'mainapp/products.html', content)
