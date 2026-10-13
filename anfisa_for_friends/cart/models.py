from django.db import models
from django.conf import settings


class Cart(models.Model):
    """
    Модель корзины.
    Привязана к пользователю (если авторизован) или к сессии (если гость).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    session_key = models.CharField(
        'Ключ сессии',
        max_length=40,
        null=True,
        blank=True,
        db_index=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username}'
        return f'Корзина (сессия {self.session_key})'

    @property
    def total_price(self):
        """Возвращает общую стоимость всех товаров в корзине."""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Модель позиции в корзине (товар + количество).
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        'ice_cream.IceCream',
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'
        unique_together = ('cart', 'product')  # один товар — одна позиция

    def __str__(self):
        return f'{self.product.title} × {self.quantity}'

    @property
    def total_price(self):
        """Стоимость позиции: цена товара × количество."""
        return self.product.price * self.quantity
