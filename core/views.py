from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, AddDeskForm, AddTaskForm, AddCommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from .models import Desk
from .models import Task, Comment


class Register(View):
    """Вью для регистрации"""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    @csrf_exempt
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
        context = {'form': form}
        return render(request, 'register.html', context)


class Login(View):
    """Вью для входа пользователя в систему"""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'login.html', {})

    @csrf_exempt
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'login.html')


class Logout(View):
    """Вью для выхода пользователя из системы"""
    def get(self, request):
        logout(request)
        return redirect('login')


class Home(LoginRequiredMixin, ListView):
    """Вью для взаимодействия с домашней страницей"""
    model = Desk
    template_name = 'home.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Desk.objects.all()
        return Desk.objects.filter(team__username=self.request.user.username)

    @csrf_exempt
    def post(self, request):
        form = AddDeskForm(request.POST)
        if form.is_valid():
            new_desk = Desk.objects.create(title=form.cleaned_data.get('deskname'))
            new_desk.team.add(request.user)
            new_desk.save()
            return redirect('home')


class DeskView(LoginRequiredMixin, View):
    """Вью для взаимодействия с доской заданий"""
    def get(self, request, pk):
        desk = Desk.objects.get(id=pk)
        if request.user not in desk.team.all():
            return redirect('home')
        tasks = Task.objects.filter(desk=desk)
        tasks0 = tasks.filter(progress=0)
        tasks1 = tasks.filter(progress=1)
        tasks2 = tasks.filter(progress=2)
        context = {'desk': desk, 'tasks0': tasks0, 'tasks1': tasks1, 'tasks2': tasks2}
        return render(request, 'desk.html', context)

    @csrf_exempt
    def post(self, request, pk):
        if 'color' in request.POST:
            form = AddTaskForm(request.POST)
            if form.is_valid():
                desk = Desk.objects.get(id=pk)
                new_task = Task.objects.create(
                    content=form.cleaned_data.get('task_title'),
                    text=form.cleaned_data.get('task_text'),
                    author=request.user,
                    desk=desk, colors=form.cleaned_data.get('color')
                )
                new_task.save()
                return redirect('desk', pk)

        elif 'username' in request.POST:
            username = request.POST.get('username')
            desk = Desk.objects.get(id=pk)
            user = User.objects.get(username=username)
            if user is not None:
                desk.team.add(user)
                desk.save()
            return redirect('desk', pk)

        elif 'leave' in request.POST:
            desk = Desk.objects.get(id=pk)
            desk.team.remove(request.user)
            desk.save()
            return redirect('home')


class TaskView(LoginRequiredMixin, View):
    """Вью для взаимодействия с заданиями"""
    def get(self, request, dpk, tpk):
        desk = Desk.objects.get(id=dpk)
        if request.user not in desk.team.all():
            return redirect('home')
        task = Task.objects.get(id=tpk)
        comments = Comment.objects.filter(task=task)
        executors = User.objects.filter(executor=task)
        context = {'desk': desk, 'task': task, 'tag': dict(task.COLOR_CHOICES).get(task.colors), 'comments': comments, 'executors': executors}
        return render(request, 'task.html', context)

    @csrf_exempt
    def post(self, request, dpk, tpk):
        if 'new_comment' in request.POST:
            form = AddCommentForm(request.POST)
            if form.is_valid():
                task = Task.objects.get(id=tpk)
                comment = Comment.objects.create(content=form.cleaned_data.get('new_comment'), author=request.user.username,
                                                 task=task)
                comment.save()
                return redirect('task', dpk, tpk)
        elif 'progress' in request.POST:
            task = Task.objects.get(id=tpk)
            task.progress += 1
            task.save()
            return redirect('desk', dpk)
        elif 'new_executor' in request.POST:
            username = request.POST.get('new_executor')
            task = Task.objects.get(id=tpk)
            user = User.objects.get(username=username)
            if user is not None:
                task.executor.add(user)
                task.save()
            return redirect('task', dpk, tpk)
