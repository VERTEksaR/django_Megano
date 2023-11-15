from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


def category_image_directory_path(instance: 'Categories', filename: str) -> str:
    return 'category/category_{pk}/image/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Categories(MPTTModel):
    class MPTTMeta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        order_insertion_by = ['title']

    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to=category_image_directory_path)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

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

    def __str__(self):
        return self.title
