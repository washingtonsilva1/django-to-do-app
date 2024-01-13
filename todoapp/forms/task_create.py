from todoapp.models import Task

from django import forms
from django.core.exceptions import ValidationError


class TaskCreateForm(forms.ModelForm):
    name = forms.CharField(
        label='Task name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: Do the laundry',
            }
        ),
        max_length=80,
        error_messages={
            'required': 'This field can not be empty.',
            'max_length': 'Your task name must have at most 80 characters.'
        }
    )

    description = forms.CharField(
        label='Task description',
        widget=forms.Textarea(),
        max_length=150,
        error_messages={
            'max_length': 'Your description must have at most 150 characters.'
        }
    )

    class Meta:
        model = Task
        exclude = ['is_completed', 'created_at', 'user']

    def clean_name(self):
        name_field = self.cleaned_data.get('name', '')
        if len(name_field) < 8:
            raise ValidationError(
                code='invalid',
                message='Your task name must have eight characters or more.'
            )
        return name_field

    def clean(self):
        cleaned_data = super().clean()
        task_name = cleaned_data.get('name', '')
        task_desc = cleaned_data.get('description', '')
        if task_name.lower() == task_desc.lower():
            raise ValidationError({
                'description': ValidationError(
                    code='invalid',
                    message='Your description can not be equal to your task name.')
            })
        return cleaned_data
