from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'publication', 'number_of_views')
    prepopulated_fields = {"slug": ("name",)}
