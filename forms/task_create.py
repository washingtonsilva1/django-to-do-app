from todoapp.models import Task

from django import forms
from django.core.exceptions import ValidationError


class TaskCreateForm(forms.ModelForm):
    name = forms.CharField(
        min_length=8,
        max_length=80,
        error_messages={
            'required': 'Your task name can not be empty.',
            'min_length': 'Your task name must have at least 8 characters.',
            'max_length': 'Your task name must have at most 80 characters.',
        }
    )

    def clean_name(self):
        cleaned_name = self.cleaned_data.get('name', '')
        task = Task.objects.filter(name=cleaned_name).order_by('id').first()
        if task is not None and task.pk != self.instance.pk:
            raise ValidationError(
                message='A task with this name already exists.',
                code='invalid'
            )
        return cleaned_name

    class Meta:
        model = Task
        exclude = ['is_completed', 'created_at', 'user']
