from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_completed']
    list_editable = ['is_completed']
