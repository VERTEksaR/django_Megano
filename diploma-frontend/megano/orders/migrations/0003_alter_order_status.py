# Generated by Django 4.2.5 on 2023-11-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_products_productsinorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=150, verbose_name='Статус'),
        ),
    ]