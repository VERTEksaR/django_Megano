# Generated by Django 4.2.5 on 2023-11-03 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_imageforproduct_name_remove_product_images_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecificationsForProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Название')),
                ('value', models.CharField(max_length=80, verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
