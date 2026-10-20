import pytest
from django.contrib.auth import get_user_model
from ice_cream.models import Category, IceCream
from reviews.models import Review

User = get_user_model()


@pytest.fixture
def category():
    """Фикстура для создания категории."""
    return Category.objects.create(name='Классическое')


@pytest.fixture
def ice_cream(category):
    """Фикстура для создания мороженого."""
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


@pytest.mark.django_db
def test_category_slug_auto_generation(category):
    """Проверка автоматической генерации слага у категории."""
    assert category.slug == 'klassicheskoe'


@pytest.mark.django_db
def test_average_rating_no_reviews(ice_cream):
    """Средний рейтинг без отзывов должен быть 0."""
    assert ice_cream.average_rating == 0
    assert ice_cream.reviews_count == 0


@pytest.mark.django_db
def test_average_rating_with_reviews(ice_cream):
    """Средний рейтинг рассчитывается корректно."""
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')

    Review.objects.create(user=user1, product=ice_cream,
                          rating=5, text='Отлично')
    Review.objects.create(user=user2, product=ice_cream,
                          rating=4, text='Хорошо')

    # (5 + 4) / 2 = 4.5
    assert ice_cream.average_rating == 4.5
    assert ice_cream.reviews_count == 2


@pytest.mark.django_db
def test_stars_with_percent(ice_cream):
    """Проверка правильного расчёта процентов для звёзд."""
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')

    Review.objects.create(user=user1, product=ice_cream,
                          rating=5, text='Отлично')
    Review.objects.create(user=user2, product=ice_cream,
                          rating=4, text='Хорошо')

    # Ожидаем: 4 полных звезды и 5-я на 50%
    assert ice_cream.stars_with_percent == [100, 100, 100, 100, 50]
