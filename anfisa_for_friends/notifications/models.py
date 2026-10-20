from django.db import models


class Subscriber(models.Model):
    """
    Модель подписчика на рассылку.
    Хранит email и дату подписки.
    """

    email = models.EmailField(
        'Email',
        unique=True,
        help_text='Email для рассылки'
    )
    is_active = models.BooleanField(
        'Активна',
        default=True,
        help_text='Получает ли подписчик письма'
    )
    created_at = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
