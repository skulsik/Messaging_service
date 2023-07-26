from urllib import request

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """ Модель клиента (данные о клиенте) """
    email = models.EmailField(max_length=60, verbose_name='Почта')
    surname = models.CharField(max_length=50, verbose_name='Фамилия пользователя')
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество пользователя')
    comments = models.CharField(max_length=255, verbose_name='Комментарии')
    user_owner = models.ForeignKey('users.user', on_delete=models.PROTECT, verbose_name='Владелец клиента')
    is_active = models.BooleanField(default=True, verbose_name='Признак отображения')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """ Модель сообщения """
    topic = models.CharField(max_length=100, verbose_name='Тема письма')
    text = models.TextField(max_length=255, verbose_name='Текст письма')
    user_owner = models.ForeignKey('users.user', on_delete=models.PROTECT, verbose_name='Владелец сообщения')

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    """ Модель рассылки (данные о рассылке, подтягивает клиента и сообщение) """
    name = models.CharField(max_length=50, verbose_name='Название рассылки')
    dtime_begin = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    dtime_end = models.DateTimeField(verbose_name='Дата и время остановки рассылки')
    frequency_list: list = [
        ('day', 'Раз в день'),
        ('week', 'Раз в неделю'),
        ('month', 'Раз в месяц'),
    ]
    frequency = models.CharField(max_length=5, choices=frequency_list, default='month', verbose_name='Переодичность рассылки')
    status_list: list = [
        ('created', 'создана'),
        ('launched', 'запущена'),
        ('completed', 'завершена'),
    ]
    status = models.CharField(max_length=9, choices=status_list, default='created', verbose_name='Статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    message = models.ForeignKey(Message, on_delete=models.PROTECT, verbose_name='Сообщение')
    user_owner = models.ForeignKey('users.user', on_delete=models.PROTECT, verbose_name='Владелец рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Признак запуска рассылки')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    """ Модель история рассылок """
    dtime_mailing = models.DateTimeField(verbose_name='Дата и время попытки')
    status_mailing = models.CharField(max_length=9, default='запущена', verbose_name='Статус рассылки')
    name = models.CharField(max_length=255, verbose_name='Название рассылки', **NULLABLE)
    server_response = models.CharField(max_length=255, verbose_name='Ответ сервера')

    def __str__(self):
        return f'{self.dtime_mailing}'

    class Meta:
        verbose_name = 'История рассылки(лог)'
        verbose_name_plural = 'История рассылок(лог)'
