from . import views

from django.urls import path


app_name = 'todoapp'

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('login/', views.LoginTemplateView.as_view(), name='login'),
]
