import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ice_cream.models import Category, IceCream
from cart.models import Order, OrderItem
from reviews.forms import ReviewForm
from reviews.models import Review, can_review

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='pass')


@pytest.fixture
def another_user():
    return User.objects.create_user(username='otheruser', password='pass')


@pytest.fixture
def ice_cream():
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
        category=category,
        image='ice_creams/test.png'
    )


@pytest.fixture
def completed_order(user, ice_cream):
    """Выполненный заказ пользователя с товаром."""
    order = Order.objects.create(
        user=user,
        first_name='Иван',
        phone='+79991234567',
        address='ул. Пушкина',
        status='completed',
        total_price=100
    )
    OrderItem.objects.create(
        order=order,
        product=ice_cream,
        product_title=ice_cream.title,
        price=100,
        quantity=1
    )
    return order


@pytest.mark.django_db
def test_can_review_with_completed_order(user, ice_cream, completed_order):
    """Отзыв можно оставить, если есть выполненный заказ."""
    assert can_review(user, ice_cream) is True


@pytest.mark.django_db
def test_can_review_without_order(user, ice_cream):
    """Отзыв нельзя оставить без выполненного заказа."""
    assert can_review(user, ice_cream) is False


@pytest.mark.django_db
def test_can_review_already_reviewed(user, ice_cream, completed_order):
    """Нельзя оставить второй отзыв на тот же товар."""
    Review.objects.create(user=user, product=ice_cream,
                          rating=5, text='Отлично')
    assert can_review(user, ice_cream) is False


@pytest.mark.django_db
def test_review_form_moderation():
    """Форма не должна пропускать запрещённые слова."""
    form_data = {
        'rating': 5,
        'text': 'Это тестовый отзыв с запрещёнкой'
    }
    form = ReviewForm(data=form_data)

    # Форма должна быть невалидной, так как слово в списке
    assert form.is_valid() is False
    assert 'text' in form.errors


@pytest.mark.django_db
def test_can_review_with_pending_order(user, ice_cream):
    """Отзыв нельзя оставить, если заказ еще не выполнен (статус new)."""
    # Создаем заказ со статусом "new" (по умолчанию)
    order = Order.objects.create(
        user=user, first_name='Иван', phone='+7999', address='ул. Пушкина',
        status='new', total_price=100
    )
    OrderItem.objects.create(
        order=order, product=ice_cream, product_title=ice_cream.title,
        price=100, quantity=1
    )

    assert can_review(user, ice_cream) is False


@pytest.mark.django_db
def test_hidden_review_not_displayed_and_not_counted(client, user, ice_cream):
    """
    Скрытый отзыв (is_published=False) не влияет
    на рейтинг и не показывается.
    """
    # Создаем скрытый отзыв с рейтингом 1
    Review.objects.create(user=user, product=ice_cream,
                          rating=1, text='Плохо', is_published=False)

    # Рейтинг должен быть 0, так как отзыв скрыт
    assert ice_cream.average_rating == 0

    # Открываем страницу товара
    url = reverse('ice_cream:ice_cream_detail', kwargs={'pk': ice_cream.id})
    response = client.get(url)

    # В контексте шаблона не должно быть текста скрытого отзыва
    assert 'Плохо' not in response.content.decode()
