from django.urls import path
from .views import Blog, BlogDetail#1 usul
from django.views.generic import TemplateView #2 usul


urlpatterns = [
    # path('blog/', blog, name='blog'),
    # path('detail-blog/<int:pk>/', detail, name='detail'),
    # path('blog/', TemplateView.as_view(template_name='blog/post_list.html'), name='blog'), #2 usul
    path('blog/', Blog.as_view(), name='blog'),
    path('detail/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
]
