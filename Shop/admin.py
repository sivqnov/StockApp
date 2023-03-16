from django.contrib import admin
from .models import Shop, Product

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'item')
    list_display_links = ('id', 'item')
    search_fields = ('item',)

admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
