from todoapp.models import Task

from django import forms
from django.core.exceptions import ValidationError


class TaskBaseForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: Do the laundry',
            }
        ),
        min_length=8,
        max_length=80,
        error_messages={
            'required': 'This field can not be empty.',
            'min_length': 'Your task name must have at least 8 characters.',
            'max_length': 'Your task name must have at most 80 characters.',
        }
    )

    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(),
        max_length=150,
        required=False,
        error_messages={
            'max_length': 'Your description must have at most 150 characters.',
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
