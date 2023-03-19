from django.contrib import admin
from .models import Shop, Product, OrderDoneStatus, Order

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'item')
    list_display_links = ('id', 'item')
    search_fields = ('item',)

class OrderDoneStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    list_display_links = ('id', 'status')
    search_fields = ('status',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'profile', 'cart_item')
    list_display_links = ('id', 'shop', 'profile', 'cart_item')
    search_fields = ('id', 'shop', 'profile', 'cart_item')

admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderDoneStatus, OrderDoneStatusAdmin)
admin.site.register(Order, OrderAdmin)
