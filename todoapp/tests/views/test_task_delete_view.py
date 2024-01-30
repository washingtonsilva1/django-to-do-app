from parameterized import parameterized
from todoapp.views import TaskDeleteView
from utils.utils import TaskMixin

from django.test import TestCase
from django.urls import resolve, reverse


class TaskDeleteViewTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': '#DummyPassw0rd',
        }
        self.user = self.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def test_task_delete_view_is_using_correct_view(self):
        view = resolve(reverse('todoapp:task_delete'))
        self.assertIs(TaskDeleteView, view.func.view_class)

    @parameterized.expand([
        ('', 404),
        ('thatisnotanumber', 404),
        ('number4ndt3xt', 404),
    ])
    def test_task_delete_view_raises_404_if_incorrect_id_was_given(self, id, status_code):
        response = self.client.post(
            reverse('todoapp:task_delete'),
            data={'id': id},
        )
        self.assertEqual(response.status_code, status_code)

    def test_task_delete_view_an_user_can_not_delete_other_user_task(self):
        task = self.create_task()
        response = self.client.post(
            reverse('todoapp:task_delete'),
            data={'id': task.id}
        )
        self.assertEqual(response.status_code, 404)

    def test_task_delete_view_deletes_a_task(self):
        task = self.create_task(user=self.user)
        response = self.client.post(
            reverse('todoapp:task_delete'),
            data={'id': task.id},
            follow=True
        )
        content = response.content.decode()
        self.assertIn('Your task has been deleted successfully!', content)
