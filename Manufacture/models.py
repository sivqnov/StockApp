from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Manufacture(models.Model):
    name = models.CharField(max_length = 150, verbose_name='Название')
    photo = models.ImageField(upload_to = 'manufacture/%Y/%m/%d/', blank=True, verbose_name='Фото')
    bio = models.TextField(blank=True, verbose_name='О предприятии')
    code = models.CharField(max_length = 16, verbose_name='Код')

    def get_absolute_url(self):
        return reverse('manufacture', kwargs={"id": self.id})

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'
        ordering = ['-name', '-bio']

class CatalogItem(models.Model):
    manufacturer = models.ForeignKey('Manufacture', on_delete=models.CASCADE, blank=False, null=True, verbose_name='Производитель')
    name = models.CharField(max_length = 150, verbose_name='Название')
    bio = models.TextField(blank=True, verbose_name='О предприятии')
    code = models.CharField(max_length = 13, verbose_name='Код товара')
    photo = models.ImageField(upload_to = 'catalog_items/%Y/%m/%d/', blank=True, verbose_name='Фото')
    date_of_manufacture = models.DateField(verbose_name='Дата производства')
    expiration_date = models.DateField(verbose_name='Годен до')
    price = models.FloatField(validators=[MinValueValidator(1)], verbose_name='Цена')

    def get_absolute_url(self):
        return reverse('catalog_item', kwargs={"id": self.id})

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name = 'Товар каталога'
        verbose_name_plural = 'Товары каталога'
        ordering = ['-name', '-id']

# CatalogItem:
# - id
# - manufacturer (FK to Manufacture)
# - name
# - bio
# - code (13 digits)
# - photo
# - date of manufacture
# - expiration date
# - price