from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to = 'avatars/%Y/%m/%d/', blank=True, verbose_name='Фото')
    bio = models.TextField(blank=True, verbose_name='О себе')
    manufactures = models.ManyToManyField('Manufacture.Manufacture', blank=True, verbose_name="Производства")

    def get_absolute_url(self):
        return reverse('user', kwargs={"user": self.user.username})

    def __str__(self):
        return f'{self.id}. {self.user}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-user', '-bio']