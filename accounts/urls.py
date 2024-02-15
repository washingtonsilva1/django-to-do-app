from . import views

from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('login/', view=views.LoginTemplateView.as_view(), name='login'),
    path('register/',
         view=views.RegisterTemplateView.as_view(),
         name='register'),
    path('logout/', view=views.LogoutView.as_view(), name='logout'),
]
