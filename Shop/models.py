from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length = 150, verbose_name='Название', unique=True)
    photo = models.ImageField(upload_to = 'shop/%Y/%m/%d/', blank=False, verbose_name='Фото')
    bio = models.TextField(blank=True, verbose_name='О магазине')
    code = models.CharField(max_length = 16, verbose_name='Код')

    def get_absolute_url(self):
        return reverse('shop', kwargs={"name": self.name})

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['-name', '-bio']

class Product(models.Model):
    item = models.ForeignKey('Manufacture.CatalogItem', on_delete=models.CASCADE, blank=False, verbose_name='Товар')
    stock = models.ForeignKey('Shop', on_delete=models.CASCADE, blank=False, verbose_name='Магазин')
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)], verbose_name='Количество')
    price = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(252734999999999.97)], verbose_name='Цена')

    def get_absolute_url(self):
        return reverse('product', kwargs={"id": self.id})
    
    def total_price(self):
        return round(self.amount * self.price)

    def __str__(self):
        return f'{self.id}. {self.item.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']

class OrderDoneStatus(models.Model):
    status = models.CharField(max_length=50, verbose_name='Статус выполнения')

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'
        ordering = ['-id']

class Order(models.Model):
    shop = models.ForeignKey('Shop', default=0, on_delete=models.PROTECT, verbose_name='Магазин')
    profile = models.ForeignKey('Members.Profile', default=0, on_delete=models.PROTECT, verbose_name='Пользователь')
    cart_item = models.ForeignKey('Members.CartItem', default=0, on_delete=models.CASCADE, verbose_name='Элемент корзины')
    phone = models.CharField(max_length=13, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    post_index = models.CharField(max_length=10, verbose_name='Почтовый индекс')
    is_done = models.ForeignKey('OrderDoneStatus', on_delete=models.PROTECT, verbose_name='Статус выполнения')

    def __str__(self):
        return f'{self.id}. {self.profile.name}, {self.cart_item.product.item.name} - {self.cart_item.amount} шт.'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']