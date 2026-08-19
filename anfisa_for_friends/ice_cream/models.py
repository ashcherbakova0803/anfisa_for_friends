from django.db import models


class Category(models.Model):
    """
    Модель категории для группировки продуктов (мороженого).

    Категории позволяют классифицировать продукты по типам, например:
        - Классическое (пломбир, ванильное)
        - Новинки (сезонные или новые вкусы)
        - Экспериментальное (необычные сочетания)

    Связана с моделью IceCream через внешний ключ (ForeignKey).
    Одна категория может содержать множество продуктов.

    Атрибуты:
        name (str): Название категории (уникальное).
        slug (str): Уникальный URL-идентификатор, генерируется автоматически
                    из названия при сохранении.
        description (str): Описание категории (необязательное поле).
    """

    name = models.CharField('Название категории', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=100, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    """
    Модель ингредиента, используемого в мороженом.
    Связана с IceCream через ManyToMany.
    """
    name = models.CharField(
        'Название ингредиента',
        max_length=100,
        unique=True,
        help_text='Уникальное название, например, "Сливки (70%)"'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class IceCream(models.Model):
    """
    Модель, представляющая продукт (мороженое).
    """
    title = models.CharField(
        'Название',
        max_length=200,
        help_text='Полное название мороженого (например, "Сырное мороженое")'
    )
    description = models.TextField(
        'Описание',
        help_text='Краткое описание вкуса или особенности'
    )
    price = models.DecimalField(
        'Цена (руб)',
        max_digits=8,
        decimal_places=2,
        help_text='Цена в рублях, например, 89.00'
    )
    weight = models.PositiveIntegerField(
        'Вес (грамм)',
        help_text='Вес порции в граммах (целое число)'
    )
    calories = models.PositiveIntegerField(
        'Калорийность (ккал)',
        help_text='Количество килокалорий'
    )
    protein = models.DecimalField(
        'Белки (г)',
        max_digits=5,
        decimal_places=2,
        help_text='Содержание белков в граммах'
    )
    fat = models.DecimalField(
        'Жиры (г)',
        max_digits=5,
        decimal_places=2,
        help_text='Содержание жиров в граммах'
    )
    carbs = models.DecimalField(
        'Углеводы (г)',
        max_digits=5,
        decimal_places=2,
        help_text='Содержание углеводов в граммах'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='ice_creams/',
        blank=True,
        null=True,
        help_text='Путь к файлу изображения продукта'
    )
    is_available = models.BooleanField(
        'В наличии',
        default=True,
        help_text='Отображать ли товар на сайте'
    )
    created_at = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        help_text='Автоматически устанавливается при создании'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ice_creams',
        verbose_name='Ингредиенты',
        blank=True,
        help_text='Выберите ингредиенты, входящие в состав'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ice_creams',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Мороженое'
        verbose_name_plural = 'Мороженое'
        ordering = ['title']

    def __str__(self):
        return self.title
