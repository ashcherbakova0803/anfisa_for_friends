import pytest
from django.urls import reverse

from about.models import ContactRequest


@pytest.mark.django_db
def test_contact_form_submission(client):
    """Форма обратной связи создает запись в БД."""
    url = reverse('about:description')

    # Проверяем, что записей нет
    assert ContactRequest.objects.count() == 0

    # Отправляем форму (как физлицо)
    response = client.post(url, {
        'name': 'Иван Иванов',
        'email': 'ivan@test.com',
        'phone': '+79991234567',
        'request_type': 'person',
        'message': 'Вопрос по доставке'
    })

    # Должен быть редирект на эту же страницу
    assert response.status_code == 302
    assert ContactRequest.objects.count() == 1

    request_obj = ContactRequest.objects.first()
    assert request_obj.name == 'Иван Иванов'
    assert request_obj.email == 'ivan@test.com'
    assert request_obj.request_type == 'person'
    assert request_obj.message == 'Вопрос по доставке'
