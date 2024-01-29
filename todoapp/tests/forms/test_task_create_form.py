from utils.utils import TaskMixin

from django.test import TestCase
from django.urls import reverse


class TaskCreateFormTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': 'DummyPassword',
        }
        self.form_data = {
            'name': 'Task Incredible Name',
            'description': 'An Incredible description for this task'
        }
        self.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def test_task_create_form_name_field_can_not_be_empty(self):
        self.form_data['name'] = ''
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        self.assertIn(
            'This field can not be empty.',
            response.context['form'].errors['name']
        )

    def test_task_create_form_name_field_must_have_at_least_eight_characters(self):
        self.form_data['name'] = 'A'*7
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        self.assertIn(
            'Your task name must have at least 8 characters.',
            response.context['form'].errors['name']
        )

    def test_task_create_form_name_field_must_have_at_most_eighty_characters(self):
        self.form_data['name'] = 'A'*81
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        self.assertIn(
            'Your task name must have at most 80 characters.',
            response.context['form'].errors['name']
        )

    def test_task_create_form_description_field_must_have_at_most_one_fifty_characters(self):
        self.form_data['description'] = 'A'*151
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        self.assertIn(
            'Your description must have at most 150 characters.',
            response.context['form'].errors['description']
        )

    def test_task_create_form_name_field_can_not_be_equal_to_an_existing_task_name(self):
        task = self.create_task(name='Yet, another task')
        self.form_data['name'] = task.name
        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data
        )
        self.assertIn(
            'A task with this name already exists.',
            response.context['form'].errors['name']
        )

    def test_task_create_form_creates_a_task_successfully(self):
        message_needed = 'Your task has been created successfully!'

        response = self.client.post(
            reverse('todoapp:task_create'),
            data=self.form_data,
            follow=True
        )
        content = response.content.decode('utf-8')
        self.assertIn(
            message_needed,
            content
        )
