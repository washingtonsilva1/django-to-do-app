from todoapp.views import CleanCompletedTasksView
from utils.utils import TaskMixin

from django.test import TestCase
from django.urls import resolve, reverse


class CleanCompletedTasksViewTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': '#Passw0rdDummy'
        }
        self.user = self.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def test_clean_completed_tasks_view_is_using_correct_view(self):
        view = resolve(reverse('todoapp:tasks_clear'))
        self.assertIs(view.func.view_class, CleanCompletedTasksView)

    def test_clean_completed_tasks_view_is_deleting_only_completed_tasks(self):
        message = 'Your completed tasks have been deleted successfully!'
        self.create_task_sample(
            n=3,
            is_completed=True,
            user=self.user
        )
        self.create_task(user=self.user)
        response = self.client.post(
            reverse('todoapp:tasks_clear'),
            follow=True
        )
        content = response.content.decode()
        self.assertEqual(len(response.context['page'].object_list), 1)
        self.assertIn(message, content)

    def test_clean_completed_tasks_view_does_nothing_if_no_completed_tasks_were_found(self):
        message = 'You do not have any completed task!'
        response = self.client.post(
            reverse('todoapp:tasks_clear'),
            follow=True
        )
        content = response.content.decode()
        self.assertIn(message, content)
