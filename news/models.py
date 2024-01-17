from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.template.defaultfilters import truncatechars
from decimal import Decimal
from typing import Any


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    user: Any
    posts: Any

    def update_rating(self):
        post_rating = self.posts.aggregate(post_rating=Sum('rating'))['post_rating'] * 3 or 0
        comment_rating = Comment.objects.filter(post__author=self).aggregate(
            comment_rating=Sum('rating')
        )['comment_rating'] or 0
        post_comment_rating = Comment.objects.filter(post__author=self).exclude(
            user=self.user
        ).aggregate(
            post_comment_rating=Sum('rating')
        )['post_comment_rating'] or 0
        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Модель для связи "многие ко многим" с моделью Category
class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    post: Any

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"


class News(models.Model):
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    text = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title  # Определяем, что использовать как строковое представление объекта


class Article(models.Model):
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    text = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


# Модель Post
class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NE'
    POST_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2, choices=POST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    title: Any

    def preview(self):
        return truncatechars(self.content, 124)

    def update_rating(self):
        total_rating = Decimal(str(self.rating)) + (Decimal(
            Comment.objects.filter(post__author=self).aggregate(total_rating=Sum('rating'))['total_rating']) or Decimal(
            0))
        self.rating = total_rating
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None)  # Добавляем связь с моделью Author
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    objects = models.Manager()
    user: Any
    post: Any

    def like(self):
        self.rating = F('rating') + 1
        self.save()

    def dislike(self):
        self.rating = F('rating') - 1
        self.save()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"