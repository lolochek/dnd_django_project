from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_article, name='create_article'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article-list/', views.article_list, name='article_list')
]