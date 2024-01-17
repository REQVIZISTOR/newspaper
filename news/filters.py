from django_filters import FilterSet, CharFilter, DateFilter
from .models import News


class NewsFilter(FilterSet):
    category = CharFilter(field_name='category__name', lookup_expr='icontains')  # Поиск по категории
    publication_date__gt = DateFilter(field_name='publication_date', lookup_expr='gt')  # Новости, опубликованные после указанной даты

    class Meta:
       model = News
       fields = {
           'title': ['icontains'],  # Поиск по названию
       }

