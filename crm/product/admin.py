from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_taxation',)
    list_editable = (['is_taxation'])
    list_filter = ('is_taxation', 'price', )


@admin.register(models.OrganizationProduct)
class OrganizationProductAdmin(admin.ModelAdmin):
    pass
