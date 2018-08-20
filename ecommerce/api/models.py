# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    description = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description


class User_e(models.Model):
    firstName = models.CharField(max_length=60)
    lastName = models.CharField(max_length=60)
    type = models.ForeignKey(UserType, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Product(models.Model):
    name = models.CharField(max_length=100)
    npc = models.CharField(max_length=60)
    description = models.TextField(default='')
    stock = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    likes = models.IntegerField(null=False, default=0)
    last_update = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class SaleHeader(models.Model):
    customer = models.ForeignKey(User_e, on_delete=models.PROTECT)
    purchase_date = models.DateField(auto_now_add=True)
    items = models.IntegerField(null=False, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)

    def __str__(self):
        return self.customer.__str__() + " - " + str(self.total)


class SaleDetail(models.Model):
    header = models.ForeignKey(SaleHeader, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False, default=0)
    unitPrice = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    fullPrice = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)

    def __str__(self):
        return self.header.pk + " - " + self.pk
