import sweetify
from .models import Task
from forms import TaskCreateForm
from utils.pagination import custom_paginator

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:login')
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


class TaskCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

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


class TaskUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

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


class TaskDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

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


class CleanCompletedTasksView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def post(self, req, *args, **kwargs):
        tasks = Task.objects.filter(
            is_completed=True,
            user=self.request.user
        )
        if len(tasks) > 0:
            tasks.delete()
            sweetify.toast(
                self.request,
                'Your completed tasks have been deleted successfully!',
                icon='success'
            )
        else:
            sweetify.toast(
                self.request,
                'You do not have any completed task!',
                icon='error'
            )
        return redirect('todoapp:home')
