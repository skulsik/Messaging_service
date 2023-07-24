import random

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from blog.models import Blog
from messaging.forms import ClientCreateViewForm, MessageCreateViewForm, MailingCreateViewForm
from messaging.models import Client, Message, Mailing


class HomeView(ListView):
    """ Главная страница """
    model = Client
    template_name = 'messaging/main.html'
    extra_context = {
        'title': ''
    }

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_active=True)
    #     return queryset

    def get_context_data(self, **kwargs):
        """ Делает набор данных из раззных моделей """
        context_data = super().get_context_data(**kwargs)
        # Передаем три статьи из блога
        blog_list = Blog.objects.filter(publication=True)
        blog_random_list = random.sample(list(blog_list), 3)
        context_data['blog1'] = blog_random_list[0]
        context_data['blog2'] = blog_random_list[1]
        context_data['blog3'] = blog_random_list[2]

        return context_data


class ClientCreateView(CreateView):
    """ Добавление нового клиента в БД """
    model = Client
    #permission_required = "catalog.add_product"
    form_class = ClientCreateViewForm

    def get_success_url(self):
        """ Берем id из данного объекта """
        return reverse_lazy('messaging:view_client', args=(self.object.id,))

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """
        # Создает форму в памяти, без отправки в бд
        self.object = form.save(commit=False)
        # Передает текущего пользователя в user
        self.object.user_owner = self.request.user
        # Сохраняет в бд
        self.object.save()
        return super(ClientCreateView, self).form_valid(form)


class ClientView(DetailView):
    """ Отображение одного клиента """
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class AllClientsView(ListView):
    """ Список клиентов """
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_owner=self.request.user)
        return queryset


class ClientDeleteView(DeleteView):
    """ Удаление клиента """
    model = Client
    success_url = reverse_lazy('messaging:clients')


class ClientUpdateView(UpdateView):
    """ Обновление информации клиента """
    model = Client
    form_class = ClientCreateViewForm
    template_name = 'messaging/client_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('messaging:update_client', args=[self.get_object().pk])


class MessageCreateView(CreateView):
    """ Добавление нового сообщения в БД """
    model = Message
    #permission_required = "catalog.add_product"
    form_class = MessageCreateViewForm

    def get_success_url(self):
        """ Берем id из данного объекта """
        return reverse_lazy('messaging:view_message', args=(self.object.id,))

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """
        # Создает форму в памяти, без отправки в бд
        self.object = form.save(commit=False)
        # Передает текущего пользователя в user
        self.object.user_owner = self.request.user
        # Сохраняет в бд
        self.object.save()
        return super(MessageCreateView, self).form_valid(form)


class MessageView(DetailView):
    """ Отображение одного сообщения """
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class AllMessagesView(ListView):
    """ Список клиентов """
    model = Message
    extra_context = {
        'title': 'Список сообщений'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_owner=self.request.user)
        return queryset


class MessageDeleteView(DeleteView):
    """ Удаление клиента """
    model = Message
    success_url = reverse_lazy('messaging:messages')


class MessageUpdateView(UpdateView):
    """ Обновление информации сообщения """
    model = Message
    form_class = MessageCreateViewForm
    template_name = 'messaging/message_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('messaging:update_message', args=[self.get_object().pk])


class AllUserMailingView(ListView):
    """ Список клиентов """
    model = Mailing
    template_name = 'messaging/user_mailing.html'
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_owner=self.request.user)
        return queryset


class MailingCreateView(CreateView):
    """ Добавление новой рассылки в БД """
    model = Mailing
    #permission_required = "catalog.add_product"
    form_class = MailingCreateViewForm

    def get_success_url(self):
        """ Берем id из данного объекта """
        return reverse_lazy('messaging:user_view_mailing', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # Получает клиентов пользователя
        client_list = Client.objects.filter(user_owner=self.request.user)
        client_list = list(client_list)
        context_data['client_list'] = client_list

        return context_data

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """
        # Создает форму в памяти, без отправки в бд
        self.object = form.save(commit=False)
        # Передает текущего пользователя в user
        self.object.user_owner = self.request.user
        # Сохраняет в бд
        self.object.save()

        # Получает клиентов пользователя
        client_list = Client.objects.filter(user_owner=self.request.user)
        client_list = list(client_list)
        # Получает POST словарь
        post_dict = dict(self.request.POST.items())
        # Строит связь clients = все клиенты пользователя
        for client in client_list:
            # Если в ПОСТ есть клиент принадлежащий пользователю добавляет связь
            if client.email in post_dict:
                self.object.clients.add(client)

        return super(MailingCreateView, self).form_valid(form)


class UserMailingView(DetailView):
    """ Отображение одной рассылки """
    model = Mailing
    template_name = 'messaging/user_mailing_view.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class UserMailingDeleteView(DeleteView):
    """ Удаление рассылки """
    model = Mailing
    success_url = reverse_lazy('messaging:user_mailing')


class UserMailingUpdateView(UpdateView):
    """ Обновление информации рассылки """
    model = Mailing
    form_class = MailingCreateViewForm
    template_name = 'messaging/mailing_form.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # Получает клиентов пользователя
        client_list = Client.objects.filter(user_owner=self.request.user)
        client_list = list(client_list)
        context_data['client_list'] = client_list

        # Получает клиентов данной рассылки
        mailing_list = list(self.object.clients.all())
        context_data['mailing_list'] = mailing_list

        return context_data

    def get_success_url(self, *args, **kwargs):
        return reverse('messaging:update_mailing', args=[self.get_object().pk])

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """

        # Получает клиентов пользователя
        client_list = Client.objects.filter(user_owner=self.request.user)
        client_list = list(client_list)

        # Получает клиентов данной рассылки
        mailing_list = list(self.object.clients.all())

        # Получает POST словарь
        post_dict = dict(self.request.POST.items())
        # Строит связь clients = все клиенты пользователя
        for client in client_list:
            # Если в ПОСТ есть клиент принадлежащий пользователю добавляет связь
            if client.email in post_dict:
                self.object.clients.add(client)
            else:
                # Если обЬект в списке не выбранных клиентов, удаляет связь
                if client in mailing_list:
                    self.object.clients.remove(client)

        return super(UserMailingUpdateView, self).form_valid(form)


class ModeratorAllMailingView(ListView):
    """ Список клиентов """
    model = Mailing
    template_name = 'messaging/moderator_mailing.html'
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.all().order_by('user_owner')
        return queryset


# class ModeratorMailingView(DetailView):
#     """ Отображение одной рассылки """
#     model = Mailing
#     template_name = 'messaging/user_mailing_view.html'
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['title'] = self.get_object()
#         return context_data
