from utils.utils import TaskMixin

import pytest
from parameterized import parameterized
from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse


@pytest.mark.fast
class RegisterFormTest(TestCase, TaskMixin):
    def setUp(self):
        self.form_data = {
            'username': 'DummyUser',
            'email': 'dummymail@mailcompany.com',
            'password': '#DummyPassw0rd',
            'password2': '#DummyPassw0rd',
        }

    def send_post(self, follow=False) -> HttpResponse:
        response = self.client.post(
            reverse('todoapp:register'),
            data=self.form_data,
            follow=follow
        )
        return response

    @parameterized.expand([
        ('username', 'This field can not be empty.'),
        ('email', 'This field can not be empty.'),
        ('password', 'This field can not be empty.'),
        ('password2', 'This field can not be empty.'),
    ])
    def test_register_form_fields_can_not_be_empty(self, field, error):
        self.form_data[field] = ''
        response = self.send_post()
        self.assertIn(error, response.context['form'].errors[field])

    def test_register_form_username_field_must_be_unique(self):
        existing_name = 'drognar'
        self.create_user(username=existing_name)
        self.form_data['username'] = existing_name
        response = self.send_post()
        self.assertIn(
            'A user with this name already exists.',
            response.context['form'].errors['username']
        )

    def test_register_form_email_field_must_be_valid(self):
        invalid_mail = 'testmail.br'
        self.form_data['email'] = invalid_mail
        response = self.send_post()
        self.assertIn(
            'Your email address must be valid.',
            response.context['form'].errors['email']
        )

    def test_register_form_password_field_must_match_the_requirements(self):
        invalid_password = 'simplepassword'
        self.form_data['password'] = invalid_password
        response = self.send_post()
        self.assertIn(
            'Your password does not match the requirements.',
            response.context['form'].errors['password']
        )

    def test_resgister_form_password2_field_must_be_equal_to_password_field(self):
        diff_password = '#SneakyPassword'
        self.form_data['password2'] = diff_password
        response = self.send_post()
        self.assertIn(
            'Your passwords are not equal.',
            response.context['form'].errors['password2']
        )

    def test_register_form_is_creating_an_user_correctly(self):
        response = self.send_post(follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Your user has been created successfully!', content)
