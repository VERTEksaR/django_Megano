# Generated by Django 4.2.5 on 2023-11-10 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_delivery_payment_alter_order_deliverytype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='price',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Цена'),
        ),
    ]
