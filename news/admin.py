from .models import Author, Category, PostCategory, News, Post, Comment
from django.contrib import admin

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(News)
admin.site.register(Post)
admin.site.register(Comment)