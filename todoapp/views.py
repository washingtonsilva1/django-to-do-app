import sweetify
from .models import Task
from .forms.login import LoginForm

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('todoapp:login')
    template_name = 'todoapp/view/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(user=self.request.user)
        ctx.update({
            'title': 'Home',
            'tasks': tasks,
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
    fields = ['name', 'description']
    template_name = 'todoapp/view/task_create.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'title': 'Task Create'
        })
        return ctx
