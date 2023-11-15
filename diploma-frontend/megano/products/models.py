from django.db import models

from catalog.models import Categories
from tags.models import Tags


def product_image_directory_path(instance: 'Product', filename: str) -> str:
    return 'product/product_{pk}/image/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Цена')
    salePrice = models.DecimalField(default=None, blank=True, null=True, max_digits=8, decimal_places=2,
                                    verbose_name='Цена при акции')
    count = models.SmallIntegerField(default=0, verbose_name='Количество')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    dateFrom = models.DateField(blank=True, null=True, verbose_name='Начало акции')
    dateTo = models.DateField(blank=True, null=True, verbose_name='Конец акции')
    title = models.CharField(max_length=100, verbose_name='Название', unique=True, db_index=True)
    description = models.CharField(max_length=150, null=True, blank=True, verbose_name='Краткое описание')
    fullDescription = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Полное описание')
    freeDelivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка')
    tags = models.ManyToManyField(Tags, verbose_name='Теги')
    purchases = models.SmallIntegerField(default=0, verbose_name='Количество покупок')
    limitedEdition = models.BooleanField(default=False, verbose_name='Ограниченный тираж')
    onSales = models.BooleanField(default=False, verbose_name='Участвует в акции')

    def __str__(self):
        return self.title


class ImageForProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to=product_image_directory_path)

    def info_image(self):
        if self.image:
            image = {
                'src': self.image.url,
                'alt': self.image.name,
            }
        else:
            image = {
                'src': '',
                'alt': '',
            }
        return image


class SpecificationsForProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name='Название')
    value = models.CharField(max_length=80, verbose_name='Значение')

    def __str__(self):
        return self.name


class ReviewForProduct(models.Model):
    author = models.CharField(max_length=150, verbose_name='Автор')
    email = models.EmailField(verbose_name='Почта')
    text = models.TextField(null=False, blank=True, verbose_name="Описание")
    rate = models.SmallIntegerField(default=5, verbose_name='Оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return f'{self.author} --- {self.rate}'
