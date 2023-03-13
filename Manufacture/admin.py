from django.contrib import admin
from .models import Manufacture, CatalogItem

# Register your models here.

class ManufactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bio', 'code')
    list_display_links = ('id', 'name', 'code')
    search_fields = ('name', 'bio',)

class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bio', 'code')
    list_display_links = ('id', 'name', 'code')
    search_fields = ('name', 'bio',)

admin.site.register(Manufacture, ManufactureAdmin)
admin.site.register(CatalogItem, CatalogItemAdmin)