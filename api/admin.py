from django.contrib import admin
from . import models


admin.site.register(models.UserType)
admin.site.register(models.User_e)
admin.site.register(models.Product)
admin.site.register(models.SaleHeader)
admin.site.register(models.SaleDetail)
