import pytest
from django.contrib.auth import get_user_model

from cart.models import CartItem
from ice_cream.models import Category, IceCream

User = get_user_model()


@pytest.fixture
def ice_cream():
    category = Category.objects.create(name='Тест')
    return IceCream.objects.create(
        title='Пломбир', description='Вкусный', price=100,
        weight=100, calories=200, protein=3.5, fat=15.0, carbs=20.5,
        category=category
    )


@pytest.mark.django_db
def test_add_same_product_twice(client, ice_cream):
    """
    Если добавить один товар дважды, увеличивается количество,
    а не создается дубль.
    """
    # Добавляем товар через URL дважды
    url_add = f'/cart/add/{ice_cream.id}/'
    client.post(url_add, {'quantity': 1})
    client.post(url_add, {'quantity': 2})

    # Проверяем корзину через базу данных
    # (так как это гость, корзина привязана к сессии)
    # В базе должна быть 1 позиция, но с quantity=3
    items = CartItem.objects.all()
    assert items.count() == 1
    assert items.first().quantity == 3


@pytest.mark.django_db
def test_update_quantity_to_zero(client, ice_cream):
    """Если количество становится 0, позиция удаляется."""
    # Добавляем товар
    url_add = f'/cart/add/{ice_cream.id}/'
    client.post(url_add, {'quantity': 2})

    # Получаем ID созданной позиции
    item = CartItem.objects.first()

    # Обновляем количество через AJAX (JSON)
    import json
    url_update = '/cart/update-ajax/'
    data = json.dumps({'item_id': item.id, 'quantity': 0})
    client.post(url_update, data, content_type='application/json')

    # Проверяем, что позиция удалилась
    assert CartItem.objects.count() == 0
