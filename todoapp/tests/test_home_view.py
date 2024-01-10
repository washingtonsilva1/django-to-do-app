from todoapp.views import HomeTemplateView
from utils.utils import create_user

from django.test import TestCase
from django.urls import resolve, reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': '#DummyPassword'
        }
        self.user = create_user(
            self.user_data['username'],
            self.user_data['password']
        )
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password']
        )

    def test_home_view_is_using_correct_view_class(self):
        view = resolve(reverse('todoapp:home'))
        self.assertIs(view.func.view_class, HomeTemplateView)

    def test_home_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('todoapp:home'))
        self.assertTemplateUsed(response, 'todoapp/view/home.html')

    def test_home_view_title_is_rendering_correctly(self):
        response = self.client.get(reverse('todoapp:home'))
        title_needed = f'{response.context["title"]} | ToDo - App'
        content = response.content.decode('utf-8')
        self.assertIn(title_needed, content)

    def test_home_view_display_default_text_if_does_not_have_any_task(self):
        response = self.client.get(reverse('todoapp:home'))
        text_needed = 'Looks like you don\'t have any task'
        content = response.content.decode('utf-8')
        self.assertIn(text_needed, content)
