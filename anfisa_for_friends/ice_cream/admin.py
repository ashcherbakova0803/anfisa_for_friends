from django.contrib import admin

from .models import IceCream, Ingredient, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(IceCream)
class IceCreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('title', 'description')
    filter_horizontal = ('ingredients',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
