from .task_form import TaskBaseForm
from todoapp.models import Task


class TaskCreateForm(TaskBaseForm):
    class Meta:
        model = Task
        exclude = ['is_completed', 'created_at', 'user']
