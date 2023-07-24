from django import template
from django.utils.safestring import mark_safe


register = template.Library()


# Шаблонный фильтр
@register.filter
def mediapath(format_path):
    """ Фильтр. Возвращает модифицированную строку """
    return mark_safe(f'http://127.0.0.1:8000/media/{format_path}')

# Шаблонный тэг
@register.simple_tag
def mediapath(format_path):
    """ Тег. Возвращает модифицированную строку """
    return f'http://127.0.0.1:8000/media/{format_path}'