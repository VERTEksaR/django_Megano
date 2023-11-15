# Generated by Django 4.2.5 on 2023-11-06 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_specificationsforproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название'),
        ),
        migrations.CreateModel(
            name='ReviewForProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=150, verbose_name='Автор')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('text', models.TextField(blank=True, verbose_name='Описание')),
                ('rate', models.SmallIntegerField(default=5, verbose_name='Оценка')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
            ],
        ),
    ]