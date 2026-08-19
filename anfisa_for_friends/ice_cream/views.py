from django.views.generic import DetailView
from django_filters.views import FilterView

from .filters import IceCreamFilter
from .models import IceCream


class IceCreamListView(FilterView):
    """
    Отображает список всех продуктов.
    """
    model = IceCream
    template_name = 'ice_cream/list.html'
    context_object_name = 'ice_cream_list'
    filterset_class = IceCreamFilter
    ordering = ['title']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class IceCreamDetailView(DetailView):
    """
    Отображает детальную информацию о продукте.
    """
    model = IceCream
    template_name = 'ice_cream/detail.html'
    context_object_name = 'ice_cream'
