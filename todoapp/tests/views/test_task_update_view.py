from todoapp.views import TaskUpdateView
from utils.utils import TaskMixin

from django.test import TestCase
from django.urls import reverse, resolve


class TaskUpdateViewTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': 'DummyPassw0rd'
        }
        self.user = self.create_user(**self.user_data)
        self.task = self.create_task(user=self.user)
        self.client.login(**self.user_data)

    def test_task_update_view_is_using_correct_view(self):
        view = resolve(reverse('todoapp:task_update', args=[self.task.pk]))
        self.assertIs(view.func.view_class, TaskUpdateView)

    def test_task_update_view_does_not_get_a_task_from_other_user(self):
        task = self.create_task(name='Yet, another task')
        response = self.client.get(
            reverse(
                'todoapp:task_update',
                args=[task.pk]
            )
        )
        self.assertEqual(404, response.status_code)

    def test_task_update_view_is_rendering_correct_template(self):
        response = self.client.get(
            reverse('todoapp:task_update', args=[self.task.pk])
        )
        self.assertTemplateUsed(response, 'todoapp/view/task_update.html')

    def test_task_update_view_title_is_displaying_correctly(self):
        title_needed = 'Update Task | ToDo - App'
        response = self.client.get(
            reverse('todoapp:task_update', args=[self.task.pk])
        )
        content = response.content.decode('utf-8')
        self.assertIn(title_needed, content)
