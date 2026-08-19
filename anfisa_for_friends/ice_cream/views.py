from django.shortcuts import render
from django.http import Http404
from .data import ice_cream_catalog

def ice_cream_detail(request, pk):
    try:
        pk = int(pk)
    except ValueError as exc:
        raise Http404("Неверный ID товара") from exc

    if pk < 0 or pk >= len(ice_cream_catalog):
        raise Http404("мороженое не найдено")

    template = 'ice_cream/detail.html'
    context = {'ice_cream': ice_cream_catalog[pk]}
    return render(request, template, context)


def ice_cream_list(request):
    template = 'ice_cream/list.html'
    context = {'ice_cream_list': ice_cream_catalog}
    return render(request, template, context)
