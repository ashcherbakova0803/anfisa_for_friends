from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Модель отзыва на товар.
    Оставить отзыв может только пользователь, который заказал этот товар
    и чей заказ имеет статус «Выполнен».
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        'ice_cream.IceCream',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар'
    )
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Оценка от 1 до 5'
    )
    text = models.TextField('Текст отзыва', max_length=1000)
    is_published = models.BooleanField(
        'Опубликован',
        default=True,
        help_text='Отображать ли отзыв на сайте'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ('user', 'product')

    def __str__(self):
        return f'Отзыв от {self.user.username} на {self.product.title}'

    @property
    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)


class ReviewImage(models.Model):
    """
    Модель фотографии, прикреплённой к отзыву.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Отзыв'
    )
    image = models.ImageField(
        'Фото',
        upload_to='reviews/',
        help_text='Фото товара или упаковки'
    )
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Фото отзыва'
        verbose_name_plural = 'Фото отзывов'

    def __str__(self):
        return f'Фото к отзыву #{self.review.id}'


def can_review(user, product):
    """
    Проверяет, может ли пользователь оставить отзыв на товар.
    """
    if not user.is_authenticated:
        return False

    from cart.models import OrderItem

    has_completed_order = OrderItem.objects.filter(
        order__user=user,
        order__status='completed',
        product=product
    ).exists()

    if not has_completed_order:
        return False

    if Review.objects.filter(user=user, product=product).exists():
        return False

    return True
