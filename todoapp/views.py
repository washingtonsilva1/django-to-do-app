from .models import Task

from django.views.generic import TemplateView


class HomeTemplateView(TemplateView):
    template_name = 'todoapp/view/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tasks = Task.objects.all()
        ctx.update({
            'title': 'Home',
            'tasks': tasks,
        })
        return ctx
