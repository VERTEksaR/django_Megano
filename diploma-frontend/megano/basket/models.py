from django.contrib.auth.models import User
from django.db import models
from products.models import Product


class BasketModel(models.Model):
    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    count = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product}'

