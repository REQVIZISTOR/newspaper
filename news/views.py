from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django_filters.views import FilterView
from .filters import NewsFilter
from .models import News
from .forms import NewsForm
from django.utils import timezone
from django.urls import reverse_lazy


# Create your views here.
class NewsList(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-publication_date']
    paginate_by = 5  # указываем количество новостей на странице


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = News
    # Используем другой шаблон — product.html
    template_name = 'news_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'


class NewsSearch(FilterView):
    filterset_class = NewsFilter
    template_name = 'news_search.html'
    paginate_by = 5


    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsCreateView(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news_create.html'
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'News'
        form.instance.publication_date = timezone.now()  # Устанавливаем текущую дату и время
        return super().form_valid(form)

class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news:news_list')


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news:news_list')


class ArticleCreateView(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'article_create.html'
    success_url = '/<int:pk>/'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'Article'
        form.instance.publication_date = timezone.now()  # Устанавливаем текущую дату и время
        return super().form_valid(form)


class ArticleEditView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')


class ArticleDeleteView(DeleteView):
    model = News
    success_url = reverse_lazy('news_list')