from datetime import timedelta

import pytest
from cart.models import Cart, CartItem, PromoCode
from cart.promo import apply_promo_to_cart
from django.contrib.auth import get_user_model
from django.utils import timezone

from ice_cream.models import Category, IceCream

User = get_user_model()


@pytest.fixture
def user():
    """Тестовый пользователь."""
    return User.objects.create_user(username='testuser', password='pass')


@pytest.fixture
def ice_cream():
    """Тестовый товар."""
    category = Category.objects.create(name='Тестовая')
    return IceCream.objects.create(
        title='Пломбир',
        description='Вкусный',
        price=100,
        weight=100,
        calories=200,
        protein=3.5,
        fat=15.0,
        carbs=20.5,
        category=category
    )


@pytest.fixture
def cart(user):
    """Корзина, привязанная к пользователю."""
    return Cart.objects.create(user=user)


@pytest.fixture
def promo():
    """Активный промокод на 15%."""
    return PromoCode.objects.create(
        code='SUMMER15',
        discount_percent=15,
        valid_until=timezone.now() + timedelta(days=10),
        is_active=True
    )


@pytest.mark.django_db
def test_promo_code_is_valid(promo):
    """Проверка, что активный промокод валиден."""
    assert promo.is_valid is True


@pytest.mark.django_db
def test_promo_code_expired(promo):
    """Проверка, что просроченный промокод невалиден."""
    promo.valid_until = timezone.now() - timedelta(days=1)
    promo.save()
    assert promo.is_valid is False


@pytest.mark.django_db
def test_promo_code_max_uses(promo):
    """Проверка, что исчерпанный промокод невалиден."""
    promo.max_uses = 1
    promo.used_count = 1
    promo.save()
    assert promo.is_valid is False


@pytest.mark.django_db
def test_apply_promo_to_cart(cart, ice_cream, promo):
    """Проверка правильного расчета скидки."""
    # Добавляем 2 товара по 100 руб. (Итого: 200)
    CartItem.objects.create(cart=cart, product=ice_cream, quantity=2)

    # Применяем промокод 15%
    totals = apply_promo_to_cart(cart, promo)

    assert totals['subtotal'] == 200
    assert totals['discount'] == 30.0  # 15% от 200
    assert totals['total'] == 170.0
