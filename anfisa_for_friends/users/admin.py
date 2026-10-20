from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения кастомной модели User в админке."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('username',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Дополнительно', {
            'fields': ('phone', 'avatar', 'bio')
        }),
        ('Права доступа', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Дополнительно', {
            'fields': ('phone', 'avatar', 'bio'),
        }),
    )
