from django.db import models
from django.db.models.functions import Lower
import django_filters
from django import forms

from .models import IceCream, Category


class IceCreamFilter(django_filters.FilterSet):
    """
    Набор фильтров для каталога мороженого.
    Позволяет фильтровать по категории и искать по названию/описанию.
    """
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории'
    )
    search = django_filters.CharFilter(
        method='filter_search',
        label='Поиск',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название или описание...'
        })
    )

    class Meta:
        model = IceCream
        fields = ['category', 'search']

    def filter_search(self, queryset, name, value):
        """
        Ищет вхождение подстроки в название или описание.
        Работает с кириллицей через перебор вариантов регистра.
        """
        value_lower = value.lower()
        value_upper = value.upper()
        value_capitalize = value.capitalize()

        return queryset.filter(
            models.Q(title__contains=value) |
            models.Q(description__contains=value) |
            models.Q(title__contains=value_lower) |
            models.Q(description__contains=value_lower) |
            models.Q(title__contains=value_upper) |
            models.Q(description__contains=value_upper) |
            models.Q(title__contains=value_capitalize) |
            models.Q(description__contains=value_capitalize)
        ).distinct()
