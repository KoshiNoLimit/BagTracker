from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_process(value):
    if value not in ['danger', 'success', 'info']:
        raise ValidationError('Error with color')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class AddDeskForm(forms.Form):
    deskname = forms.CharField(label='deskname', min_length=3, max_length=20)


class AddTaskForm(forms.Form):
    task_text = forms.CharField(label='task_text', min_length=5, max_length=200)
    color = forms.CharField(label='color', validators=[validate_process])


class AddCommentForm(forms.Form):
    new_comment = forms.CharField(label='new_comment', max_length=200)