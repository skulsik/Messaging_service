from django.urls import path
from django.views.generic import TemplateView

#from django.views.decorators.cache import cache_page

from messaging.apps import MessagingConfig
from messaging.views import *

app_name = MessagingConfig.name

urlpatterns = [
    path('', TemplateView.as_view(template_name='messaging/main.html'), name='home')
]