# Generated by Django 4.1.7 on 2023-03-15 21:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Manufacture', '0003_alter_catalogitem_bio_alter_catalogitem_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('photo', models.ImageField(blank=True, upload_to='shop/%Y/%m/%d/', verbose_name='Фото')),
                ('bio', models.TextField(blank=True, verbose_name='О магазине')),
                ('code', models.CharField(max_length=16, verbose_name='Код')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'ordering': ['-name', '-bio'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(252735000000000)], verbose_name='Количество')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(252734999999999.97)], verbose_name='Цена')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manufacture.catalogitem', verbose_name='Товар')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop.shop', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-id'],
            },
        ),
    ]
