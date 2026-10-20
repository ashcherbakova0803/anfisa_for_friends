from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Форма оформления заказа.
    Запрашивает контактные данные и адрес доставки.
    """

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone',
                  'email', 'address', 'comment')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иван'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванов'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ivan@example.com'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Город, улица, дом, квартира'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Комментарий к заказу (необязательно)'
            }),
        }
