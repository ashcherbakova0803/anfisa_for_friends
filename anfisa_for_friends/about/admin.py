from django.contrib import admin
from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'request_type', 'email',
                    'created_at', 'is_processed')
    list_filter = ('request_type', 'is_processed', 'created_at')
    search_fields = ('name', 'email', 'message')
