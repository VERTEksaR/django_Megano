from django.contrib.auth.models import User
from django.db import models


def profile_avatar_directory_path(instance: 'Profile', filename: str) -> str:
    return 'profiles/profile_{pk}/avatar/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.CharField(max_length=75, verbose_name='Электронная почта', unique=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path)

    def info_avatar(self):
        if self.avatar:
            avatar = {
                'src': self.avatar.url,
                'alt': self.avatar.name,
            }
        else:
            avatar = {
                'src': '',
                'alt': '',
            }
        return avatar
