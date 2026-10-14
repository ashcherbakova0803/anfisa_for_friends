from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Форма для создания отзыва.
    Позволяет поставить оценку, написать текст и прикрепить одно фото.
    """
    image = forms.ImageField(
        label='Фото',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        required=False,
        help_text='Прикрепите фото товара (необязательно)'
    )

    class Meta:
        model = Review
        fields = ('rating', 'text')
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} ★') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь впечатлениями о мороженом...'
            }),
        }
