# Generated by Django 4.1.7 on 2023-03-17 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0002_alter_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='photo',
            field=models.ImageField(upload_to='shop/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
