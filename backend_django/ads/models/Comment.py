from django.contrib.auth import get_user_model
from django.db import models


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='comments', verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.ad} - {self.author}: {self.text[:20]}'
