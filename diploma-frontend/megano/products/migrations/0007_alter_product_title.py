# Generated by Django 4.2.5 on 2023-11-06 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_title_reviewforproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название'),
        ),
    ]
