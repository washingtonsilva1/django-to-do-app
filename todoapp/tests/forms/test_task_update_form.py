from utils.utils import TaskMixin

from parameterized import parameterized
from django.test import TestCase
from django.urls import reverse


class TaskUpdateFormTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': 'DummyPassw0rd'
        }
        self.user = self.create_user(**self.user_data)
        self.create_task(user=self.user)
        self.form_data = {
            'name': 'New Task Name',
            'description': 'New Task Description',
            'is_completed': 'False'
        }
        self.client.login(**self.user_data)

    @parameterized.expand([
        ('name', 'This field can not be empty.'),
        ('is_completed', 'This field can not be empty.'),
    ])
    def test_task_update_form_task_fields_can_not_be_empty(self, field, error):
        self.form_data[field] = ''
        response = self.client.post(
            reverse('todoapp:task_update', args=[1]),
            data=self.form_data
        )
        self.assertIn(error, response.context['form'].errors[field])

    def test_task_update_form_task_name_must_have_at_least_eight_characters(self):
        self.form_data['name'] = 'A'*7
        response = self.client.post(
            reverse('todoapp:task_update', args=[1]),
            data=self.form_data,
        )
        self.assertIn(
            'Your task name must have at least 8 characters.',
            response.context['form'].errors['name'],
        )

    @parameterized.expand([
        ('name', 'Your task name must have at most 80 characters.'),
        ('description', 'Your description must have at most 150 characters.'),
    ])
    def test_task_update_form_task_fields_max_length(self, field, error):
        self.form_data[field] = 'A'*152
        response = self.client.post(
            reverse('todoapp:task_update', args=[1]),
            data=self.form_data,
        )
        self.assertIn(
            error,
            response.context['form'].errors[field],
        )

    def test_task_update_form_name_field_can_not_be_equal_to_an_existing_task_name(self):
        task = self.create_task(name='This task is awesome', user=self.user)
        self.form_data['name'] = task.name
        response = self.client.post(
            reverse('todoapp:task_update', args=[1]),
            data=self.form_data,
        )
        self.assertIn(
            'A task with this name already exists.',
            response.context['form'].errors['name'],
        )

    def test_task_update_form_task_is_updating_a_task(self):
        response = self.client.post(
            reverse('todoapp:task_update', args=[1]),
            data=self.form_data,
            follow=True,
        )
        content = response.content.decode('utf-8')
        self.assertIn(
            'Your task has been updated successfully!',
            content,
        )
