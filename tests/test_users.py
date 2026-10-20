import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.fixture
def user_data():
    """Данные для регистрации пользователя."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'StrongPassword123!',
        'password2': 'StrongPassword123!',
    }


@pytest.mark.django_db
def test_user_registration(client, user_data):
    """Проверка успешной регистрации пользователя."""
    # Убеждаемся, что пользователя еще нет
    assert User.objects.count() == 0

    # Отправляем POST-запрос на страницу регистрации
    url = reverse('users:register')
    response = client.post(url, data=user_data)

    # Должен быть редирект на главную (302)
    assert response.status_code == 302
    assert User.objects.count() == 1

    user = User.objects.first()
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('StrongPassword123!')


@pytest.mark.django_db
def test_user_login(client, user_data):
    """Проверка успешного входа в систему."""
    # Сначала создаем пользователя напрямую в БД
    User.objects.create_user(
        username='testuser',
        password='StrongPassword123!'
    )

    # Отправляем POST на страницу входа
    url = reverse('login')
    response = client.post(url, {
        'username': 'testuser',
        'password': 'StrongPassword123!'
    })

    # Успешный вход перенаправляет на главную
    assert response.status_code == 302
    # Проверяем, что пользователь залогинен (в сессии есть ID)
    assert '_auth_user_id' in client.session


@pytest.mark.django_db
def test_profile_access_requires_login(client):
    """Неавторизованный пользователь не может зайти в ЛК."""
    # Создаем любого пользователя, чтобы знать его username
    user = User.objects.create_user(username='testuser', password='pass')

    url = reverse('users:profile', kwargs={'username': user.username})
    response = client.get(url)

    # Должен быть редирект на страницу логина
    assert response.status_code == 302
    assert '/auth/login/' in response.url


@pytest.mark.django_db
def test_profile_access_authorized(client, user_data):
    """Авторизованный пользователь видит свой профиль."""
    user = User.objects.create_user(username='testuser', password='pass')
    client.force_login(user)  # Принудительный вход для теста

    url = reverse('users:profile', kwargs={'username': user.username})
    response = client.get(url)

    # Должна открыться страница (200 OK)
    assert response.status_code == 200
    # Проверяем, что в контексте шаблона передан правильный пользователь
    assert response.context['profile_user'] == user
