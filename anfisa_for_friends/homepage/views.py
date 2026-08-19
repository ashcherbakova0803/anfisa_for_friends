from django.shortcuts import render
from ice_cream.data import ice_cream_catalog


def index(request):
    template = 'homepage/index.html'
    hits = ice_cream_catalog[:3]
    context = {'hits': hits}
    return render(request, template, context)
