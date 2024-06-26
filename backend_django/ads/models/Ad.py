from django.contrib.auth import get_user_model
from django.db import models

from utils.const import NULLABLE


class Ad(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название товара')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(upload_to='ads_images/', **NULLABLE, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
