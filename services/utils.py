import random
import string
from uuid import uuid4
from pytils.translit import slugify


def generation_password():
    """ Генератор пароля """
    characterList: str = ''
    characterList += string.ascii_letters
    new_password: list = []
    for i in range(20):
        # Выбирает случайный символ, из списка символов
        randomchar: chr = random.choice(characterList)
        # Добавляет выбранный символ
        new_password.append(randomchar)
    # Склеивает список символов в строку
    new_password: str = "".join(new_password)
    return new_password


def unique_slugify(instance, slug):
    """ Генератор уникальных SLUG для моделей, в случае существования такого SLUG. """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug
