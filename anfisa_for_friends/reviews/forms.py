from django import forms
from django.core.exceptions import ValidationError

from .models import Review
from .moderation import contains_forbidden_words


class ReviewForm(forms.ModelForm):
    """
    Форма для создания отзыва.
    Проверяет текст на запрещённые слова.
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

    def clean_text(self):
        """
        Проверяет текст отзыва на запрещённые слова.
        Если найдено — выбрасывает ValidationError.
        """
        text = self.cleaned_data.get('text', '')

        if contains_forbidden_words(text):
            raise ValidationError(
                'Ваш отзыв содержит недопустимые слова. '
                'Пожалуйста, переформулируйте.'
            )

        return text
