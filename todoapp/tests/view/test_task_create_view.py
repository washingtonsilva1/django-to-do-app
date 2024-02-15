from utils.utils import TaskMixin
from todoapp.views import TaskCreateView

from django.test import TestCase
from django.urls import resolve, reverse


class TaskCreateViewTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': 'DummyPassword',
        }
        self.form_data = {
            'name': 'Task Incredible Name',
        }
        self.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def test_task_create_view_is_using_correct_class(self):
        view = resolve(reverse('todoapp:task_create'))
        self.assertIs(view.func.view_class, TaskCreateView)

    def test_task_create_form_name_field_can_not_be_empty(self):
        self.form_data['name'] = ''
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        content = response.content.decode()
        self.assertIn(
            'Your task name can not be empty.',
            content
        )

    def test_task_create_form_name_field_must_have_at_least_eight_characters(self):
        self.form_data['name'] = 'A'*7
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        content = response.content.decode()
        self.assertIn(
            'Your task name must have at least 8 characters.',
            content
        )

    def test_task_create_form_name_field_must_have_at_most_eighty_characters(self):
        self.form_data['name'] = 'A'*81
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        content = response.content.decode()
        self.assertIn(
            'Your task name must have at most 80 characters.',
            content
        )

    def test_task_create_form_name_field_can_not_be_equal_to_an_existing_task_name(self):
        task = self.create_task(name='Yet, another task')
        self.form_data['name'] = task.name
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True,
        )
        content = response.content.decode()
        self.assertIn(
            'A task with this name already exists.',
            content
        )

    def test_task_create_form_creates_a_task_successfully(self):
        message_needed = 'Your task has been created successfully!'

        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        content = response.content.decode()
        self.assertIn(
            message_needed,
            content
        )
