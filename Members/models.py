from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class CartItem(models.Model):
    product = models.ForeignKey('Shop.Product', on_delete=models.CASCADE, blank=False, verbose_name='Товар')
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Количество')

    def __str__(self):
        return f'{self.id}. {self.product}'
    
    def total(self):
        return round(self.product.price * self.amount, 2)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        ordering = ['-id', '-product']

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to = 'avatars/%Y/%m/%d/', blank=False, verbose_name='Фото')
    bio = models.TextField(blank=True, verbose_name='О себе')
    manufactures = models.ManyToManyField('Manufacture.Manufacture', blank=True, verbose_name="Производства")
    shops = models.ManyToManyField('Shop.Shop', blank=True, verbose_name="Магазины")
    cart = models.ManyToManyField('CartItem', blank=True, verbose_name='Корзина')

    def get_absolute_url(self):
        return reverse('user', kwargs={"user": self.user.username})

    def __str__(self):
        return f'{self.id}. {self.user}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-user', '-bio']