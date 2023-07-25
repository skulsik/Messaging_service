from django.urls import path
from django.views.decorators.cache import cache_page

from messaging.apps import MessagingConfig
from messaging.views import *

app_name = MessagingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('clients/', cache_page(60)(AllClientsView.as_view()), name='clients'),
    path('clients/create/', ClientCreateView.as_view(), name='create_client'),
    path('clients/client/<int:pk>',  cache_page(600)(ClientView.as_view()), name='view_client'),
    path('clients/client/delete/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('clients/client/update/<int:pk>', ClientUpdateView.as_view(), name='update_client'),

    path('messages/', cache_page(60)(AllMessagesView.as_view()), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='create_message'),
    path('messages/message/<int:pk>', cache_page(600)(MessageView.as_view()), name='view_message'),
    path('messages/message/delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    path('messages/message/update/<int:pk>', MessageUpdateView.as_view(), name='update_message'),

    path('mailing/', cache_page(60)(AllUserMailingView.as_view()), name='user_mailing'),
    path('mailing/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/view/<int:pk>', cache_page(600)(UserMailingView.as_view()), name='user_view_mailing'),
    path('mailing/delete/<int:pk>', UserMailingDeleteView.as_view(), name='delete_mailing'),
    path('mailing/update/<int:pk>', UserMailingUpdateView.as_view(), name='update_mailing'),

    path('moderator/mailing/', ModeratorAllMailingView.as_view(), name='moderator_mailing'),
    path('moderator/users/', ModeratorAllUsersView.as_view(), name='moderator_users'),
]
