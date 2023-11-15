# Generated by Django 4.2.5 on 2023-10-30 23:52

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageForProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to=products.models.product_image_directory_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, to='products.imageforproduct'),
        ),
    ]