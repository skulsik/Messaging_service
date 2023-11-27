from django import forms

from blog.models import Blog
from services.forms import FormStyleMixin


class BlogCreateViewForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания клиента """
    class Meta:
        model = Blog
        fields = ('name', 'content', 'image', 'date_of_creation')
