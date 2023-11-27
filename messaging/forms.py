from django import forms

from messaging.models import Client, Message, Mailing
from services.forms import FormStyleMixin


class ClientCreateViewForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания клиента """
    class Meta:
        model = Client
        fields = ('email', 'surname', 'name', 'patronymic', 'comments')


class MessageCreateViewForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания сообщения """
    class Meta:
        model = Message
        fields = ('topic', 'text')


class MailingCreateViewForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания рассылки """
    class Meta:
        model = Mailing
        fields = ('name', 'dtime_begin', 'dtime_end', 'frequency', 'message')
