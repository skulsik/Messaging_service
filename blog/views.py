from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from blog.forms import BlogCreateViewForm
from blog.models import Blog


class BlogsView(ListView):
    """ Все блоги с активной публикацией """
    model = Blog
    template_name = 'blog/blogs.html'
    extra_context = {
        'title': 'Статьи'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication=True)
        return queryset


class UserBlogsView(ListView):
    """ Все блоги данного пользователя """
    model = Blog
    extra_context = {
        'title': 'Статьи'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_owner=self.request.user)
        return queryset


class BlogCreateView(CreateView):
    """ Создание блога """
    model = Blog
    form_class = BlogCreateViewForm

    def get_success_url(self):
        """ Берем slug из данного объекта """
        print()
        return reverse_lazy('blog:view_blog', args=(self.object.slug,))

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """
        # Создает форму в памяти, без отправки в бд
        self.object = form.save(commit=False)
        # Передает текущего пользователя в user
        self.object.user_owner = self.request.user
        # Сохраняет в бд
        self.object.save()
        return super(BlogCreateView, self).form_valid(form)


class BlogUpdateView(UpdateView):
    """ Обновление блога """
    model = Blog
    form_class = BlogCreateViewForm
    success_url = reverse_lazy('blog:blogs')


class BlogDeleteView(DeleteView):
    """ Удаление блога """
    model = Blog
    success_url = reverse_lazy('blog:blogs')


class BlogView(DetailView):
    """ Отображение блога без каких либо прав """
    model = Blog
    extra_context = {
        'title': 'Статья'
    }

    def get_object(self, queryset=None):
        """ Получает объект, увеличивает просмотры """
        object_blog = super().get_object()
        object_blog.number_of_views += 1
        object_blog.save()
        return object_blog


class UserBlogView(DetailView):
    """ Отображение одного блога принадлежащего данному пользователю """
    model = Blog
    template_name = 'blog/user_blog.html'
    extra_context = {
        'title': 'Статья'
    }
