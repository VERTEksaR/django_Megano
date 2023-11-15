# Generated by Django 4.2.5 on 2023-10-23 17:21

import authentication.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150, verbose_name='ФИО')),
                ('email', models.CharField(max_length=75, verbose_name='Электронная почта')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=authentication.models.profile_avatar_directory_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]