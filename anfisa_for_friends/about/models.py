from django.db import models


class ContactRequest(models.Model):
    """Модель заявки с формы обратной связи."""

    REQUEST_TYPES = [
        ('person', 'Физлицо'),
        ('company', 'Юрлицо'),
    ]

    name = models.CharField('Имя / Название компании', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    request_type = models.CharField(
        'Тип обращения',
        max_length=20,
        choices=REQUEST_TYPES,
        default='person'
    )
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.get_request_type_display()})'
