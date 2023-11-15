# Generated by Django 4.2.5 on 2023-11-10 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=150, verbose_name='ФИО')),
                ('email', models.CharField(max_length=75, verbose_name='Электронная почта')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('createdAd', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('deliveryType', models.CharField(max_length=50, verbose_name='Тип доставки')),
                ('paymentType', models.CharField(max_length=100, verbose_name='Тип оплаты')),
                ('totalCost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('status', models.CharField(max_length=50, verbose_name='Статус')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('address', models.CharField(max_length=150, verbose_name='Адрес')),
                ('products', models.ManyToManyField(to='basket.basketmodel', verbose_name='Товары')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]