import sweetify
from .models import Task
from .forms import LoginForm, TaskCreateForm, TaskUpdateForm, RegisterForm
from utils.pagination import custom_paginator

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('todoapp:login')
    template_name = 'todoapp/view/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        additional_query = self.request.GET.get('q', '')
        tasks = Task.objects.filter(user=self.request.user).order_by('-id')
        if additional_query:
            tasks = tasks.filter(
                Q(
                    Q(name__icontains=additional_query) |
                    Q(description__icontains=additional_query)
                )
            )
            ctx.update({
                'additional_query': f'&q={additional_query}',
                'search_term': additional_query
            })
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


class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('todoapp:login')
    model = Task
    template_name = 'todoapp/view/task_create.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('todoapp:home')

    def post(self, req, *args, **kwargs):
        return super().post(req, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        sweetify.toast(
            self.request,
            'Your task has been created successfully!',
            icon='success'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'title': 'Create Task',
        })
        return ctx


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('todoapp:login')
    success_url = reverse_lazy('todoapp:home')
    model = Task
    form_class = TaskUpdateForm
    template_name = 'todoapp/view/task_update.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'title': 'Update Task',
        })
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def form_valid(self, form):
        sweetify.toast(
            self.request,
            'Your task has been updated successfully!',
            icon='success'
        )
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('todoapp:login')

    def get_task(self, task_id: str):
        if not task_id.isdigit():
            raise Http404()
        return get_object_or_404(Task, id=task_id, user=self.request.user)

    def post(self, req, *args, **kwargs):
        task_id = self.request.POST.get('id', '')
        task = self.get_task(task_id)
        task.delete()
        sweetify.toast(
            self.request,
            'Your task has been deleted successfully!',
            icon='success'
        )
        return redirect('todoapp:home')
