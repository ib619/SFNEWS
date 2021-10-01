from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

User.objects.all().delete()
Author.objects.all().delete()
Category.objects.all().delete()
Post.objects.all().delete()
Comment.objects.all().delete()

