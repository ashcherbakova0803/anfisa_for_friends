from django.contrib import admin
from .models import Review, ReviewImage


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating', 'created_at')
    search_fields = ('user__username', 'product__title', 'text')
    inlines = (ReviewImageInline,)
