import django_filters

from .models import IceCream, Category


class IceCreamFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории'
    )

    class Meta:
        model = IceCream
        fields = ['category']
