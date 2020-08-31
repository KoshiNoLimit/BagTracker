from django.db import models
from django.contrib.auth.models import User


class Desk(models.Model):
    title = models.CharField(max_length=30)
    team = models.ManyToManyField(User)


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    RED, GREEN, BLUE = 'danger', 'success', 'info'
    COLOR_CHOICES = ((RED, 'Red'), (GREEN, 'Green'), (BLUE, 'Blue'))
    colors = models.CharField(max_length=7, choices=COLOR_CHOICES, default=BLUE)
    progress = models.PositiveSmallIntegerField(default=0)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)



# Добавить комментарии
