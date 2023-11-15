from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Delivery(models.Model):
    class Meta:
        verbose_name = 'Тип доставки'
        verbose_name_plural = 'Типы доставок'

    type = models.CharField(max_length=8, verbose_name='Тип доставки')
    freePrice = models.PositiveSmallIntegerField(default=0,
                                                 verbose_name='Мин. цена для бесплатной доставки')
    tax = models.PositiveSmallIntegerField(default=0, verbose_name='Плата за доставку')

    def __str__(self):
        return self.type


class Payment(models.Model):
    class Meta:
        verbose_name = 'Вид платежа'
        verbose_name_plural = 'Виды платежей'

    type = models.CharField(max_length=7, verbose_name='Тип оплаты')

    def __str__(self):
        return self.type


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'заказы'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    fullName = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.CharField(max_length=75, verbose_name='Электронная почта')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    createdAd = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    deliveryType = models.ForeignKey(Delivery, on_delete=models.DO_NOTHING, verbose_name='Тип доставки')
    paymentType = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, verbose_name='Тип оплаты')
    totalCost = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Цена')
    status = models.CharField(max_length=150, verbose_name='Статус')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=150, verbose_name='Адрес')


class ProductsInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')




