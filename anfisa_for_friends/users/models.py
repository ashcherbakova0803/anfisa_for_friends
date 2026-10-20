from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Расширяет стандартную AbstractUser дополнительными полями.
    """

    phone = models.CharField(
        'Телефон',
        max_length=20,
        blank=True,
        help_text='Контактный номер телефона'
    )
    address = models.TextField(
        'Адрес доставки',
        max_length=300,
        blank=True,
        help_text='Адрес по умолчанию для доставки заказов'
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Фото профиля'
    )
    bio = models.TextField(
        'О себе',
        max_length=500,
        blank=True,
        help_text='Краткая информация о пользователе'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
