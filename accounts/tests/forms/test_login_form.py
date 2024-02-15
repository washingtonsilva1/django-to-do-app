from parameterized import parameterized
from utils.utils import TaskMixin


from django.urls import reverse
from django.test import TestCase


class LoginFormTest(TestCase, TaskMixin):
    def setUp(self):
        self.form_data = {
            'username': 'DummyUser',
            'password': 'DummyPassword',
        }

    @parameterized.expand([
        ('username', 'This field can not be empty.'),
        ('password', 'This field can not be empty.'),
    ])
    def test_login_form_fields_can_not_be_empty(self, field, error):
        self.form_data[field] = ''
        response = self.client.post(
            reverse('accounts:login'),
            data=self.form_data,
            follow=True
        )
        self.assertIn(error, response.context['form'].errors[field])

    def test_login_form_user_not_found(self):
        response = self.client.post(
            reverse('accounts:login'),
            data=self.form_data,
            follow=True,
        )
        content = response.content.decode('utf-8')
        self.assertIn('User not found', content)
        self.assertIn('Incorrect username or password', content)

    def test_login_form_authenticate_user(self):
        self.create_user(**self.form_data)
        response = self.client.post(
            reverse('accounts:login'),
            data=self.form_data,
        )
        self.assertRedirects(response, reverse('todoapp:home'))
