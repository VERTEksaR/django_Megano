# Generated by Django 4.2.5 on 2023-11-10 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_delivery_freeprice_delivery_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='price',
        ),
    ]
