from . import views

from django.urls import path


app_name = 'todoapp'

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('login/', views.LoginTemplateView.as_view(), name='login'),
    path('register/', views.RegisterTemplateView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/clear/', views.TasksClearView.as_view(), name='tasks_clear'),
]
