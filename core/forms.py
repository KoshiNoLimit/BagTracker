from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_process(value):
    if value not in ['danger', 'success', 'info']:
        raise ValidationError('Error with color')


class CreateUserForm(UserCreationForm):
    """форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class AddDeskForm(forms.Form):
    """форма добавления доски заданий"""
    deskname = forms.CharField(label='deskname', min_length=3, max_length=50)


class AddTaskForm(forms.Form):
    """форма добавления задания"""
    task_text = forms.CharField(label='task_text', min_length=5, max_length=1000)
    task_title = forms.CharField(label='task_title', min_length=5, max_length=200)
    color = forms.CharField(label='color', validators=[validate_process])


class AddCommentForm(forms.Form):
    """форма добавления комментария"""
    new_comment = forms.CharField(label='new_comment', max_length=200)