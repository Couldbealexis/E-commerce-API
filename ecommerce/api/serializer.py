from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')


class User_eSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = User_e
        fields = ('id', 'firstName', 'lastName', 'type', 'user')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'npc', 'description', 'stock', 'price', 'likes', 'last_update')


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
