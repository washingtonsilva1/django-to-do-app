import sweetify
from .models import Task
from .forms import LoginForm, TaskCreateForm
from utils.pagination import custom_paginator

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login


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
        POST = self.request.POST
        self.request.session['form_post_data'] = POST
        form = LoginForm(POST)
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
                del (self.request.session['form_post_data'])
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
            return redirect('todoapp:login')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form_post_data = self.request.session.get('form_post_data', None)
        form = LoginForm(form_post_data)
        ctx.update({
            'title': 'Login',
            'form': form,
        })
        return ctx


class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('todoapp:login')
    model = Task
    template_name = 'todoapp/view/task_create.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('todoapp:home')

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
            'title': 'Task Create',
        })
        return ctx
