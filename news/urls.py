from django.urls import path
from .views import NewsList, NewsDetail


app_name = 'news'

urlpatterns = [
    path('list/', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
]