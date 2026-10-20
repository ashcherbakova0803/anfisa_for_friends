from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ContactForm


def description(request):
    """
    Страница «Контакты».
    Отображает информацию о компании и форму обратной связи.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение отправлено!')
            return redirect('about:description')
    else:
        form = ContactForm()

    return render(request, 'about/description.html', {
        'form': form,
        'yandex_maps_api_key': settings.YANDEX_MAPS_API_KEY,
        'debug_mode': settings.DEBUG,
    })
