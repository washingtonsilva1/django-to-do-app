from . import views

from django.urls import path


app_name = 'todoapp'

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('login/', views.LoginTemplateView.as_view(), name='login'),
    path('register/', views.RegisterTemplateView.as_view(), name='register'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(),
         name='task_update'),
]
