from django.urls import path
from .views import (
    NewsList,
    NewsDetail,
    NewsSearch,
    NewsCreateView,
    NewsUpdateView,
    NewsDeleteView,
    ArticleCreateView,
    ArticleEditView,
    ArticleDeleteView,
    subscriptions,
)


app_name = 'news'

urlpatterns = [
    path('list/', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/update/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/update/', ArticleEditView.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]