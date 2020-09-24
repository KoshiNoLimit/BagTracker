from django.db import models
from django.contrib.auth.models import User


class Desk(models.Model):
    """доска с заданиями"""
    title = models.CharField(max_length=50)
    team = models.ManyToManyField(User)


class Task(models.Model):
    """задание"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    RED, GREEN, BLUE = 'danger', 'success', 'info'
    COLOR_CHOICES = ((RED, 'Error'), (GREEN, 'Idea'), (BLUE, 'Weak'))
    colors = models.CharField(max_length=7, choices=COLOR_CHOICES, default=BLUE)
    progress = models.PositiveSmallIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)
    executor = models.ManyToManyField(User, related_name='executor')


class Comment(models.Model):
    """комментарий к заданию"""
    content = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
