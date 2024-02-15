from accounts.views import RegisterTemplateView
from utils.utils import TaskMixin
from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpResponse


class RegisterViewTest(TestCase, TaskMixin):
    def send_get(self) -> HttpResponse:
        response = self.client.get(reverse('accounts:register'))
        return response

    def test_register_view_is_using_correct_view_class(self):
        view = resolve(reverse('accounts:register'))
        self.assertIs(view.func.view_class, RegisterTemplateView)

    def test_register_view_is_rendering_correct_template(self):
        response = self.send_get()
        self.assertTemplateUsed(response, 'accounts/view/register.html')

    def test_register_view_redirects_to_home_if_user_is_logged_in(self):
        user_data = {
            'username': 'dummyuser',
            'password': 'dummypassword'
        }
        self.create_user(**user_data)
        self.client.login(**user_data)
        response = self.send_get()
        self.assertRedirects(response, reverse('todoapp:home'))
