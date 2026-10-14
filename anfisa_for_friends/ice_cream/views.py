from django.conf import settings
from django.views.generic import DetailView

from django_filters.views import FilterView

from reviews.models import can_review
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
    paginate_by = settings.PAGINATE_BY_CATALOG

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class IceCreamDetailView(DetailView):
    """
    Отображает детальную информацию о продукте.
    Показывает последние отзывы и поддерживает сортировку.
    """
    model = IceCream
    template_name = 'ice_cream/detail.html'
    context_object_name = 'ice_cream'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['can_review'] = can_review(self.request.user, self.object)
        else:
            context['can_review'] = False

        # Отзывы с сортировкой
        reviews = self.object.reviews.filter(is_published=True).select_related(
            'user'
        ).prefetch_related('images')

        sort = self.request.GET.get('sort', 'newest')
        if sort == 'oldest':
            reviews = reviews.order_by('created_at')
        elif sort == 'positive':
            reviews = reviews.order_by('-rating', '-created_at')
        elif sort == 'negative':
            reviews = reviews.order_by('rating', '-created_at')
        else:
            reviews = reviews.order_by('-created_at')

        context['reviews'] = reviews[:settings.REVIEWS_ON_PRODUCT_PAGE]
        context['current_sort'] = sort

        return context
