from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    #users#
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/read/', adminapp.UserListView.as_view(), name='users'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('users/read/<page>/', adminapp.UserListView.as_view(), name='page'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),
    path('users/orders/<int:pk>/', adminapp.UserOrderListView.as_view(), name='user_orders'),
    path('users/order/<user_pk>/<int:order_pk>/<status_pk>/', adminapp.change_order_status, name='change_status'),




    # path('users/create/', adminapp.user_create, name='user_create'),
    # path('users/read/', adminapp.users, name='users'),
    # path('users/read/<page>/', adminapp.users, name='page'),
    # path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    # path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    #categories#
    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),
    path('categories/read/', adminapp.ProductCategoryListView.as_view(), name='categories'),
    path('categories/read/<page>/', adminapp.ProductCategoryListView.as_view(), name='cpage'),

    # path('categories/create/', adminapp.category_create, name='category_create'),
    # path('categories/read/', adminapp.categories, name='categories'),
    # path('categories/read/<page>/', adminapp.categories, name='cpage'),
    # path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    # path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),

    #products#
    path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product'),
    path('products/read/category/<int:pk>/', adminapp.ProductListView.as_view(), name='products'),
    path('products/read/category/<int:pk>/<page>/', adminapp.ProductListView.as_view(), name='ppage'),
    path('products/create/category/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),

    # path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    # path('products/read/category/<int:pk>/', adminapp.products, name='products'),
    # path('products/read/category/<int:pk>/<page>/', adminapp.products, name='ppage'),
    # path('products/read/<int:pk>/', adminapp.product, name='product'),
    # path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    # path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
]