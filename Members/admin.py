from django.contrib import admin
from .models import Profile, CartItem

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    search_fields = ('user',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'amount')
    list_display_links = ('id', 'product', 'amount')
    search_fields = ('id', 'product')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CartItem, CartItemAdmin)