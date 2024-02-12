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
        self.form_data = {
            'task_id': self.task.pk,
        }
        self.client.login(**self.user_data)

    def test_task_update_view_is_using_correct_view(self):
        view = resolve(reverse('todoapp:task_update'))
        self.assertIs(view.func.view_class, TaskUpdateView)

    def test_task_update_view_does_not_update_a_task_from_other_user(self):
        task = self.create_task(name='Yet, another task')
        response = self.client.post(
            reverse('todoapp:task_update'),
            data={'task_id': task.pk}
        )
        self.assertEqual(404, response.status_code)

    def test_task_update_view_is_updating_a_task_status(self):
        response = self.client.post(
            reverse('todoapp:task_update'),
            data=self.form_data,
            follow=True,
        )
        content = response.content.decode()
        self.assertIn(
            'Your task status has been updated successfully!',
            content,
        )
