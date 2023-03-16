from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length = 150, verbose_name='Название', unique=True)
    photo = models.ImageField(upload_to = 'shop/%Y/%m/%d/', blank=True, verbose_name='Фото')
    bio = models.TextField(blank=True, verbose_name='О магазине')
    code = models.CharField(max_length = 16, verbose_name='Код')

    def get_absolute_url(self):
        return reverse('shop', kwargs={"name": self.name})

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['-name', '-bio']

class Product(models.Model):
    item = models.ForeignKey('Manufacture.CatalogItem', on_delete=models.CASCADE, blank=False, verbose_name='Товар')
    stock = models.ForeignKey('Shop', on_delete=models.CASCADE, blank=False, verbose_name='Магазин')
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(252735000000000)], verbose_name='Количество')
    price = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(252734999999999.97)], verbose_name='Цена')

    def get_absolute_url(self):
        return reverse('product', kwargs={"id": self.id})

    def __str__(self):
        return f'{self.id}. {self.item.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']
