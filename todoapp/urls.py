from . import views

from django.urls import path


app_name = 'todoapp'

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/completed/',
         views.CleanCompletedTasksView.as_view(),
         name='tasks_clear'),
]
