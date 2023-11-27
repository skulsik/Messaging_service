from django.db import models
from services.utils import unique_slugify

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """ Модель статьи (блога) """
    name = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=255, verbose_name='url')
    content = models.TextField(max_length=1000, verbose_name='содержимое')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    date_of_creation = models.DateTimeField(verbose_name='дата создания')
    publication = models.BooleanField(default=False, verbose_name='признак публикации')
    user_owner = models.ForeignKey('users.user', on_delete=models.PROTECT, verbose_name='Владелец клиента')
    number_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.name}'

    def delete(self, using=None, keep_parents=False):
        """ Удаление статьи """
        self.publication = False
        self.save()

    def save(self, *args, **kwargs):
        """ Сохранение полей модели при их отсутствии заполнения """
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
