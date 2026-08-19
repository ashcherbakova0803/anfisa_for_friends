from django.shortcuts import render

from ice_cream.models import IceCream


def index(request):
    template = 'homepage/index.html'
    hits = IceCream.objects.filter(is_available=True)[:3]
    context = {'hits': hits}
    return render(request, template, context)
