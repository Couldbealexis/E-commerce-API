from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')
        fields = ('username', 'email')


class User_eSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = User_e
        fields = ('id', 'firstName', 'lastName', 'type', 'user')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'npc', 'description', 'stock', 'price', 'likes', 'last_update')


class PaginatedProductSerializer:
    def __init__(self, products, request, num):
        paginator = Paginator(products, num)
        page = request.GET.get('page','1')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        count = paginator.count

        previous = None if not products.has_previous() else products.previous_page_number()
        next = None if not products.has_next() else products.next_page_number()
        serializer = ProductSerializer(products, many=True)
        self.data = {'count': count, 'previous': previous,
                     'next': next, 'products': serializer.data}


class SaleHeaderSerializer(serializers.ModelSerializer):
    customer = User_eSerializer()
    class Meta:
        model = SaleHeader
        fields = ('id', 'customer', 'purchase_date', 'items', 'total')


class SaleDetailSerializer(serializers.ModelSerializer):
    header = SaleHeaderSerializer()
    product = ProductSerializer()
    class Meta:
        model = SaleDetail
        fields = ('id', 'header', 'product', 'quantity', 'unitPrice', 'fullPrice')
