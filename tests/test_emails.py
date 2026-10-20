import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from cart.models import Order, OrderItem
from ice_cream.models import Category, IceCream
from notifications.emails import (
    send_newsletter,
    send_order_confirmation,
    send_review_request,
)
from notifications.models import Subscriber

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser', email='test@example.com', password='pass')


@pytest.fixture
def ice_cream():
    category = Category.objects.create(name='Тест')
    return IceCream.objects.create(
        title='Пломбир', description='Вкусный', price=100,
        weight=100, calories=200, protein=3.5, fat=15.0, carbs=20.5,
        category=category
    )


@pytest.fixture
def order(user, ice_cream):
    """Создаем тестовый заказ."""
    order = Order.objects.create(
        user=user,
        first_name='Иван',
        email='test@example.com',
        phone='+79991234567',
        address='ул. Тестовая',
        status='new',
        total_price=100
    )
    OrderItem.objects.create(
        order=order, product=ice_cream, product_title=ice_cream.title,
        price=100, quantity=1
    )
    return order


@pytest.mark.django_db
def test_send_order_confirmation(order):
    """Письмо о заказе успешно отправляется."""
    # Очищаем исходящие письма перед тестом
    mail.outbox = []

    send_order_confirmation(order)

    assert len(mail.outbox) == 1
    assert 'Заказ №' in mail.outbox[0].subject
    assert 'test@example.com' in mail.outbox[0].to


@pytest.mark.django_db
def test_send_review_request(order):
    """Письмо-приглашение к отзыву отправляется."""
    mail.outbox = []

    send_review_request(order)

    assert len(mail.outbox) == 1
    assert 'впечатлениями' in mail.outbox[0].subject
    assert 'test@example.com' in mail.outbox[0].to


@pytest.mark.django_db
def test_send_newsletter():
    """Рассылка уходит всем активным подписчикам."""
    mail.outbox = []

    # Создаем подписчиков
    Subscriber.objects.create(email='sub1@test.com', is_active=True)
    Subscriber.objects.create(email='sub2@test.com', is_active=True)
    Subscriber.objects.create(email='unsub@test.com',
                              is_active=False)  # Не должен получить

    count = send_newsletter(
        subject='Новости',
        template_name='notifications/emails/promo_summer.txt'
    )

    assert count == 2
    assert len(mail.outbox) == 1
    assert 'sub1@test.com' in mail.outbox[0].to
    assert 'sub2@test.com' in mail.outbox[0].to
    assert 'unsub@test.com' not in mail.outbox[0].to
