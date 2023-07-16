import random
import string


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