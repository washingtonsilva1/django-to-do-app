from utils.utils import TaskMixin
from todoapp.views import TaskCreateView

from django.test import TestCase
from django.urls import resolve, reverse


class TaskCreateViewTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'dummyuser',
            'password': 'dummypassword',
        }
        self.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def test_task_create_view_is_using_correct_class(self):
        view = resolve(reverse('todoapp:task_create'))
        self.assertIs(view.func.view_class, TaskCreateView)

    def test_task_create_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('todoapp:task_create'))
        self.assertTemplateUsed(response, 'todoapp/view/task_create.html')

    def test_task_create_view_title_is_displaying_correctly(self):
        title_needed = 'Create Task | ToDo - App'

        response = self.client.get(reverse('todoapp:task_create'))
        content = response.content.decode('utf-8')
        self.assertIn(title_needed, content)
