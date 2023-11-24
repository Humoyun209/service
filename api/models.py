from django.contrib.auth.models import User
from django.db import models


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='media/Advertisement/%Y/%m/%d')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='advertisements')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='requests')
    content = models.TextField()
    created = models.DateTimeField(auto_now=True)
    is_pleasant = models.BooleanField(default=False)

    def __str__(self):
        return f'From user "{self.user.username}" to {self.advertisement.title}'