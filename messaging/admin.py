from django.contrib import admin

from messaging.models import Client, Mailing, Message, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'comments', 'is_active', 'user_owner')
    list_filter = ('user_owner',)
    search_fields = ('email', 'is_active')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'user_owner')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'text', 'user_owner')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('dtime_mailing', 'status_mailing')
