from django import forms
from .models import News, Article

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text', 'category']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'category']