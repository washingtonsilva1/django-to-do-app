from .models import Task

from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    def get(self, req, *args, **kwargs):
        tasks = Task.objects.all()
        return render(
            self.request,
            'todoapp/view/home.html',
            {
                'title': 'Home',
                'tasks': tasks,
            }
        )
