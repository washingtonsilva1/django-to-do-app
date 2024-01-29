from todoapp.models import Task
from .task_form import TaskBaseForm
from django import forms


class TaskUpdateForm(TaskBaseForm):
    is_completed = forms.ChoiceField(
        label='Status',
        required=True,
        choices=[
            ('True', 'Completed'),
            ('False', 'Pending'),
        ],
        error_messages={
            'invalid_choice': 'Your status is not valid! Please, select another one.',
            'required': 'This field can not be empty.',
        }
    )

    class Meta:
        model = Task
        exclude = ['created_at', 'user']
