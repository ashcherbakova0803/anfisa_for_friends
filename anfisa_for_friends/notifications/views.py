from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import SubscriberForm


@require_POST
def subscribe(request):
    """Подписка на рассылку."""
    form = SubscriberForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Вы успешно подписались на рассылку!')
    else:
        messages.error(
            request, 'Проверьте email — возможно, вы уже подписаны.')
    return redirect(request.META.get('HTTP_REFERER', 'homepage:index'))
