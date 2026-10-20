import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ice_cream.models import Category, IceCream

User = get_user_model()


@pytest.fixture
def user_a():
    return User.objects.create_user(username='user_a', password='pass')


@pytest.fixture
def user_b():
    return User.objects.create_user(username='user_b', password='pass')


@pytest.mark.django_db
def test_cannot_view_another_users_order(client, user_a, user_b):
    """Пользователь А не может посмотреть историю заказов пользователя Б."""
    # Создаем заказ для пользователя Б
    from cart.models import Order
    order_b = Order.objects.create(
        user=user_b, first_name='Б', phone='+7', address='А', total_price=100)

    # Логинимся как пользователь А
    client.force_login(user_a)

    # Пытаемся получить доступ к заказу Б (например, через повтор заказа)
    url = reverse('cart:order_repeat', kwargs={'order_id': order_b.id})
    response = client.post(url)

    # Ожидаем 404, так как заказ принадлежит другому
    assert response.status_code == 404


@pytest.mark.django_db
def test_catalog_pagination(client):
    """Проверка работы пагинации в каталоге."""
    category = Category.objects.create(name='Тест')
    # Создаем 7 товаров
    for i in range(7):
        IceCream.objects.create(
            title=f'Товар {i}', description='Описание', price=100,
            weight=100, calories=200, protein=3.5, fat=15.0, carbs=20.5,
            category=category,
            image='ice_creams/test.png'
        )

    url = reverse('ice_cream:ice_cream_list')

    # Первая страница (должно быть 6 товаров, так как PAGINATE_BY_CATALOG = 6)
    response1 = client.get(url)
    assert response1.status_code == 200
    assert len(response1.context['ice_cream_list']) == 6
    assert response1.context['is_paginated'] is True

    # Вторая страница (должен быть 1 товар)
    response2 = client.get(url + '?page=2')
    assert response2.status_code == 200
    assert len(response2.context['ice_cream_list']) == 1
