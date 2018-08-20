from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product'),
    path('users/', views.user_list, name='users'),
    path('buy/', views.buy_products, name='buy'),
    path('sales/', views.sales, name='sales'),
    path('sales/<int:pk>/', views.sale_detail, name='saleDetail'),
    path('like/<int:pk>/', views.like, name='like')
]