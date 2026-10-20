import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from cart.cart import CartService
from cart.models import Order
from ice_cream.models import Category, IceCream

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser', password='pass', email='test@test.com')


@pytest.fixture
def ice_cream():
    category = Category.objects.create(name='Тест')
    return IceCream.objects.create(
        title='Пломбир', description='Вкусный', price=100,
        weight=100, calories=200, protein=3.5, fat=15.0, carbs=20.5,
        category=category
    )


@pytest.mark.django_db
def test_order_creation_clears_cart(client, user, ice_cream):
    """При оформлении заказа корзина очищается, а заказ создается."""
    client.force_login(user)

    # Кладем товар в корзину
    url_add = f'/cart/add/{ice_cream.id}/'
    client.post(url_add, {'quantity': 1})

    # Оформляем заказ
    url_order = '/cart/order/create/'
    response = client.post(url_order, {
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'phone': '+79991234567',
        'email': 'test@test.com',
        'address': 'ул. Тестовая, 1',
        'comment': 'Быстрее'
    })

    assert response.status_code == 302  # Редирект на успех

    # Проверяем заказ
    order = Order.objects.first()
    assert order is not None
    assert order.user == user
    assert order.total_price == 100
    assert order.items.count() == 1

    # Проверяем, что корзина пуста
    cart = CartService(request=response.wsgi_request).cart
    assert cart.items.count() == 0


@pytest.mark.django_db
def test_apply_invalid_promo_code(client):
    """Применение несуществующего промокода возвращает ошибку."""
    url = reverse('cart:apply_promo')
    response = client.post(
        url,
        data=json.dumps({'code': 'FAKECODE'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    data = response.json()
    assert data['success'] is False
    assert 'не найден' in data['error']


@pytest.mark.django_db
def test_guest_order_creation(client, ice_cream):
    """Гость может оформить заказ, он создается без привязки к user."""
    # Добавляем товар в корзину (гость)
    client.post(f'/cart/add/{ice_cream.id}/', {'quantity': 1})

    # Оформляем заказ
    response = client.post('/cart/order/create/', {
        'first_name': 'Гость',
        'phone': '+79990000000',
        'email': 'guest@test.com',
        'address': 'ул. Гостевая',
    })

    assert response.status_code == 302
    order = Order.objects.first()
    assert order is not None
    assert order.user is None  # Заказ без пользователя
    assert order.first_name == 'Гость'
