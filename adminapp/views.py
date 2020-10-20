from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователь / создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'update_form': user_form
    }
    return render(request, 'adminapp/user_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', 'username')
    content = {
        'title': title,
        'objects': users_list,
    }
    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователь / редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:
        user_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': user_form,
    }
    return render(request, 'adminapp/user_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователь / удаление'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_user.is_active = False
        edit_user.save()
        return HttpResponseRedirect(reverse('admin:users'))


    content = {
        'title': title,
        'user_to_delete': edit_user,
    }
    return render(request, 'adminapp/user_delete.html', content)



@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категория / создание'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:category_create'))
    else:
        category_form = ProductCategoryEditForm()

    content = {
        'title': title,
        'update_form': category_form
    }
    return render(request, 'adminapp/category_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'категории'

    categories_list = ProductCategory.objects.all().order_by('-is_active', 'name')

    content = {
        'title': title,
        'objects': categories_list,
    }

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категория / редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
    else:
        category_form = ProductCategoryEditForm(instance=edit_category)

    content = {
        'title': title,
        'update_form': category_form,
    }
    return render(request, 'adminapp/category_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категория / удаление'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        if edit_category.is_active:
            edit_category.is_active = False
        else:
            edit_category.is_active = True
        edit_category.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    content = {
        'title': title,
        'category_to_delete': edit_category,
    }
    return render(request, 'adminapp/category_delete.html', content)



@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт / создание'

    category_item = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:product_create', args=[category_item.pk]))
    else:
        product_form = ProductEditForm()

    content = {
        'title': title,
        'update_form': product_form,
        'category': category_item,
    }

    return render(request, 'adminapp/product_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'продукты'

    category_item = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category=category_item).order_by('-is_active', 'name')

    content = {
        'title': title,
        'category': category_item,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product(request, pk):
    title = 'продукт'

    product_item = get_object_or_404(Product, pk=pk)
    category_item = get_object_or_404(ProductCategory, pk=product_item.category.pk)

    content ={
        'title': title,
        'product': product_item,
        'category': category_item,
    }

    return render(request, 'adminapp/product.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт / редактирование'
    product_item = get_object_or_404(Product, pk=pk)
    category_item = get_object_or_404(ProductCategory, pk=product_item.category.pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=product_item)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[product_item.pk]))
    else:
        product_form = ProductEditForm(instance=product_item)

    content = {
        'title': title,
        'update_form': product_form,
        'category': category_item
    }
    return render(request, 'adminapp/product_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт / удаление'

    product_item = get_object_or_404(Product, pk=pk)
    category_item = get_object_or_404(ProductCategory, pk=product_item.category.pk)

    if request.method == 'POST':
        if product_item.is_active:
            product_item.is_active = False
        else:
            product_item.is_active = True
        product_item.save()
        return HttpResponseRedirect(reverse('admin:products', args=[category_item.pk]))

    content = {
        'title': title,
        'product_to_delete': product_item,
        'category': category_item,
    }
    return render(request, 'adminapp/product_delete.html', content)