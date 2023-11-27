from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import *

app_name = BlogConfig.name

urlpatterns = [
    path('blogs/', cache_page(60)(BlogsView.as_view()), name='blogs'),
    path('blogs/user/', UserBlogsView.as_view(), name='user_blogs'),
    path('blogs/create/', cache_page(600)(BlogCreateView.as_view()), name='create_blog'),
    path('blogs/user_blog/<slug:slug>', UserBlogView.as_view(), name='user_view_blog'),
    path('blogs/blog/<slug:slug>', BlogView.as_view(), name='view_blog'),
    path('blogs/blog/delete/<slug:slug>', BlogDeleteView.as_view(), name='delete_blog'),
    path('blogs/blog/update/<slug:slug>', BlogUpdateView.as_view(), name='update_blog')
]
