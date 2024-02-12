import sweetify
from .models import Task
from .forms import LoginForm, TaskCreateForm, RegisterForm
from utils.pagination import custom_paginator

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Q
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('todoapp:login')
    template_name = 'todoapp/view/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(user=self.request.user).order_by('-id')
        paginator = custom_paginator(
            request=self.request,
            query_set=tasks,
            objects_per_page=settings.OBJECTS_PER_PAGE,
            pages_to_display=settings.PAGES_TO_DISPLAY,
        )
        ctx.update({
            'title': 'Home',
            'page_range': paginator['page_range'],
            'page': paginator['page'],
        })
        return ctx


class LoginTemplateView(TemplateView):
    template_name = 'todoapp/view/login.html'

    def get(self, req, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todoapp:home')
        return super().get(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        form = LoginForm(self.request.POST or None)
        if form.is_valid():
            user_auth = authenticate(
                self.request,
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', ''),
            )
            if user_auth is not None:
                sweetify.toast(
                    self.request,
                    'You have been logged in successfully!',
                    icon='success'
                )
                login(self.request, user_auth)
                return redirect('todoapp:home')
            else:
                sweetify.error(
                    self.request,
                    title='User not found',
                    text='Incorrect username or password.',
                    persistent='Close'
                )
                return redirect('todoapp:login')
        else:
            return self.get(req, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = LoginForm(self.request.POST or None)
        ctx.update({
            'title': 'Login',
            'form': form,
        })
        return ctx


class RegisterTemplateView(TemplateView):
    template_name = 'todoapp/view/register.html'

    def get(self, req, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todoapp:home')
        return super().get(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        form = RegisterForm(self.request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            sweetify.toast(
                self.request,
                'Your user has been created successfully!',
                icon='success',
            )
            return redirect('todoapp:login')
        return self.get(req, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = RegisterForm(self.request.POST or None)
        ctx.update({
            'form': form,
            'title': 'Register',
        })
        return ctx


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('todoapp:login')

    def post(self, req, *args, **kwargs):
        u = self.request.POST.get('user', None)
        if u is None or u is not None and \
                not u == self.request.user.get_username():
            return redirect('todoapp:home')
        logout(self.request)
        sweetify.toast(
            self.request,
            'You have been logged out successfully!',
            icon='success'
        )
        return redirect('todoapp:login')


class TaskCreateView(View):
    def post(self, req, *args, **kwargs):
        task_form = TaskCreateForm(self.request.POST or None)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = self.request.user
            task.save()
            sweetify.toast(
                self.request,
                title='Your task has been created successfully!',
                icon='success'
            )
        else:
            error = task_form.errors['name'][0]
            sweetify.error(
                self.request,
                title='Sorry, but...',
                text=error,
                button='Close'
            )
        return redirect("todoapp:home")


class TaskUpdateView(View):
    def get_task(self, task_id: str):
        if not task_id.isdigit():
            raise Http404()
        return get_object_or_404(Task, id=task_id, user=self.request.user)

    def post(self, request, *args, **kwargs):
        task_id = self.request.POST.get('task_id', '')
        task = self.get_task(task_id)
        task.is_completed = not task.is_completed
        task.save()
        sweetify.toast(
            self.request,
            title='Your task status has been updated successfully!',
            icon='success'
        )
        return redirect("todoapp:home")


class TaskDeleteView(View):
    def get_task(self, task_id: str):
        if not task_id.isdigit():
            raise Http404()
        return get_object_or_404(Task, id=task_id, user=self.request.user)

    def post(self, req, *args, **kwargs):
        task_id = self.request.POST.get('task_id', '')
        task = self.get_task(task_id)
        task.delete()
        sweetify.toast(
            self.request,
            'Your task has been deleted successfully!',
            icon='success'
        )
        return redirect('todoapp:home')
