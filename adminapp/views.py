from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

#-------------------CBV----------------------------------------------------
#--------------------------users------------------------------------------#
from orderapp.models import Order

def change_order_status(request, user_pk, order_pk, status_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if status_pk == 'FM':
        order.status = Order.FORMING
    elif status_pk == 'STP':
        order.status = Order.SENT_TO_PROCEED
    elif status_pk == 'PRD':
        order.status = Order.PROCEEDED
    elif status_pk == 'PD':
        order.status = Order.PAID
    elif status_pk == 'RDY':
        order.status = Order.READY
    elif status_pk == 'DN':
        order.status = Order.DONE
    else:
        order.status = Order.CANCEL
    order.save()
    return HttpResponseRedirect(reverse('adminapp:user_orders', args=user_pk))

class UserOrderListView(ListView):
    model = ShopUser
    template_name = 'adminapp/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(ShopUser, id=self.kwargs.get('pk'))
        statuses = list(map(list, Order.ORDER_STATUSES))
        context['object_list'] = Order.objects.filter(user=self.kwargs.get('pk'))
        context['user'] = user
        context['order_status'] = statuses
        return context

class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    paginate_by = 2
    ordering = '-is_superuser'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        print(self.request.__dict__)
        return context

class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


#--------------------------categories--------------------------------------#
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        print(context)
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

#-------------------------products-----------------------------------------
class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Товар Подробнее'
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('pk', None)
        if category is not None:
            context['category'] = get_object_or_404(ProductCategory, pk=category)
        return context

    def get_queryset(self):
        category = self.kwargs.get('pk', None)
        if category is not None:
            product_items = Product.objects.filter(category_id=category)
            return product_items
        return Product.objects.all()

class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('pk', None)
        if category is not None:
            context['category'] = get_object_or_404(ProductCategory, pk=category)
            context['form']['category'].initial = category
        return context

    def get_success_url(self):
        category = self.object.category.pk
        return reverse_lazy('admin:products', kwargs={'pk': category})


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category.pk
        if category is not None:
            context['category'] = get_object_or_404(ProductCategory, pk=category)
        return context

    def get_success_url(self):
        category = self.object.category.pk
        # print(category)
        return reverse_lazy('admin:products', kwargs={'pk': category})

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin:products')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        category = self.object.category.pk
        return reverse_lazy('admin:products', kwargs={'pk': category})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

#--------------------FBV----------------------------------------------------
'''
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
def users(request, page=1):
    title = 'пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', 'username')

    paginator = Paginator(users_list, 2)
    try:
        users_paginator = paginator.page(page)
    except PageNotAnInteger:
        users_paginator = paginator.page(1)
    except EmptyPage:
        users_paginator = paginator.page(paginator.num_pages)


    content = {
        'title': title,
        'objects': users_paginator,
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
def categories(request, page=1):
    title = 'категории'

    categories_list = ProductCategory.objects.all().order_by('-is_active', 'name')

    paginator = Paginator(categories_list, 2)
    try:
        categories_paginator = paginator.page(page)
    except PageNotAnInteger:
        categories_paginator = paginator.page(1)
    except EmptyPage:
        categories_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': title,
        'objects': categories_paginator,
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
        product_form = ProductEditForm(initial={'category': category_item})

    content = {
        'title': title,
        'update_form': product_form,
        'category': category_item,
    }

    return render(request, 'adminapp/product_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk, page=1):
    title = 'продукты'

    category_item = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category=category_item).order_by('-is_active', 'name')

    paginator = Paginator(products_list, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)


    content = {
        'title': title,
        'category': category_item,
        'objects': products_paginator,
    }

    return render(request, 'adminapp/products.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product(request, pk):
    title = 'продукт'
    product_item = get_object_or_404(Product, pk=pk)
    content ={
        'title': title,
        'product': product_item,
    }
    return render(request, 'adminapp/product.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт / редактирование'
    product_item = get_object_or_404(Product, pk=pk)

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
        'category': product_item.category
    }
    return render(request, 'adminapp/product_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт / удаление'

    product_item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if product_item.is_active:
            product_item.is_active = False
        else:
            product_item.is_active = True
        product_item.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product_item.category.pk]))

    content = {
        'title': title,
        'product_to_delete': product_item,
    }
    return render(request, 'adminapp/product_delete.html', content)'''
