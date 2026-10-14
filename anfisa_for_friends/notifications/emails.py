from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Subscriber


def _send_email(subject, template_name, context, recipient_list):
    """
    Внутренняя утилита для отправки письма.
    Рендерит текстовый шаблон и отправляет через send_mail.
    """
    message = render_to_string(template_name, context)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=True,
    )


def send_order_confirmation(order):
    """
    Отправляет письмо с подтверждением заказа.
    """
    if not order.email:
        return
    _send_email(
        subject=f'Заказ №{order.id} оформлен — Анфиса для друзей',
        template_name='notifications/emails/order_confirmation.txt',
        context={'order': order},
        recipient_list=[order.email],
    )


def send_welcome_email(user):
    """
    Отправляет приветственное письмо после регистрации.
    """
    if not user.email:
        return
    _send_email(
        subject='Добро пожаловать в «Анфису для друзей»!',
        template_name='notifications/emails/welcome.txt',
        context={'user': user},
        recipient_list=[user.email],
    )


def send_newsletter(subject, template_name, context=None):
    """
    Отправляет рассылку всем активным подписчикам.
    Возвращает количество отправленных писем.
    """
    subscribers = Subscriber.objects.filter(is_active=True)
    emails = [s.email for s in subscribers]
    if not emails:
        return 0

    _send_email(
        subject=subject,
        template_name=template_name,
        context=context or {},
        recipient_list=emails,
    )
    return len(emails)


def send_review_request(order):
    """
    Отправляет письмо с просьбой оставить отзыв.
    Вызывается, когда заказ получает статус «Выполнен».
    """
    if not order.email:
        return

    items = order.items.select_related('product').all()
    if not items:
        return

    _send_email(
        subject=f'Поделитесь впечатлениями о заказе №{order.id}',
        template_name='notifications/emails/review_request.txt',
        context={
            'order': order,
            'items': items,
        },
        recipient_list=[order.email],
    )
