from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from notifications.emails import send_review_request
from .models import Order


@receiver(pre_save, sender=Order)
def track_status_change(sender, instance, **kwargs):
    """
    Запоминает предыдущий статус заказа, чтобы понять,
    изменился ли он на «Выполнен».
    """
    if not instance.pk:
        instance._previous_status = None
        return

    try:
        old_order = Order.objects.get(pk=instance.pk)
        instance._previous_status = old_order.status
    except Order.DoesNotExist:
        instance._previous_status = None


@receiver(post_save, sender=Order)
def send_review_email_on_completed(sender, instance, created, **kwargs):
    """
    Отправляет письмо с просьбой оставить отзыв,
    когда статус заказа меняется на «Выполнен».
    """
    if created:
        return

    previous = getattr(instance, '_previous_status', None)
    if previous != 'completed' and instance.status == 'completed':
        send_review_request(instance)
