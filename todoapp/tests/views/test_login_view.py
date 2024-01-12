from todoapp.views import LoginTemplateView
from utils.utils import TaskMixin

from django.test import TestCase
from django.urls import reverse, resolve


class LoginViewTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': '#DummyPassw0rd'
        }
        self.create_user(
            username=self.user_data['username'],
            password=self.user_data['password']
        )

    def login_user(self):
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password'],
        )

    def test_login_view_is_loading_correct_view(self):
        view = resolve(reverse('todoapp:login'))
        self.assertIs(view.func.view_class, LoginTemplateView)

    def test_login_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('todoapp:login'))
        self.assertTemplateUsed(response, 'todoapp/view/login.html')

    def test_login_view_template_is_rendering_correct_title(self):
        title_needed = 'Login | ToDo - App'
        response = self.client.get(reverse('todoapp:login'))
        content = response.content.decode('utf-8')
        self.assertIn(title_needed, content)

    def test_login_view_redirects_to_home_if_logged(self):
        self.login_user()
        response = self.client.get(reverse('todoapp:login'))
        self.assertRedirects(response, reverse('todoapp:home'))
