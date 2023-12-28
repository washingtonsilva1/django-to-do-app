from todoapp.views import HomeTemplateView
from django.test import TestCase
from django.urls import resolve, reverse


class HomeViewTest(TestCase):
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
