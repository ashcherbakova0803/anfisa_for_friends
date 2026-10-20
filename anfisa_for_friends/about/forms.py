from django import forms

from .models import ContactRequest


class ContactForm(forms.ModelForm):
    """
    Форма обратной связи.
    """
    class Meta:
        model = ContactRequest
        fields = ('name', 'email', 'phone', 'request_type', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'request_type': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваш вопрос или предложение...'}),
        }
