from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_stars(percentages):
    """
    Рендерит 5 звёзд с частичным заполнением.
    Принимает список процентов [100, 100, 100, 100, 80].
    """
    html = '<div class="stars-container">'
    for percent in percentages:
        html += (
            '<span class="star-wrapper">'
            '<i class="far fa-star star-empty"></i>'
            f'<span class="star-filled" style="width: {percent}%">'
            '<i class="fas fa-star"></i>'
            '</span>'
            '</span>'
        )
    html += '</div>'
    return mark_safe(html)
