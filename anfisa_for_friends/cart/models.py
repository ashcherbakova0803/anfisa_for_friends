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


class Order(models.Model):
    """
    Модель заказа.
    Создаётся при оформлении корзины.
    """
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Пользователь'
    )
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True)
    address = models.TextField('Адрес доставки')
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    total_price = models.DecimalField(
        'Итоговая сумма',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ №{self.id} от {self.created_at:%d.%m.%Y}'

    @property
    def total_items(self):
        """Общее количество товаров в заказе."""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """
    Модель позиции заказа (товар + количество + цена на момент заказа).
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        'ice_cream.IceCream',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Товар'
    )
    product_title = models.CharField('Название товара', max_length=200)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.product_title} × {self.quantity}'

    @property
    def total_price(self):
        """Стоимость позиции: цена × количество."""
        return self.price * self.quantity
