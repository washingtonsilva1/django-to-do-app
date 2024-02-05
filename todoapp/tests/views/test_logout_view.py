from todoapp.views import LogoutView
from utils.utils import TaskMixin

from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpResponse


class LogoutViewTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'dummyuser',
            'password': 'dummypassword',
        }
        self.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def send_post(self, follow=False) -> HttpResponse:
        response = self.client.post(
            reverse('todoapp:logout'),
            data={
                'user': self.user_data['username']
            },
            follow=follow
        )
        return response

    def test_logout_view_is_using_correct_view_class(self):
        view = resolve(reverse('todoapp:logout'))
        self.assertIs(view.func.view_class, LogoutView)

    def test_logout_view_redirects_to_home_if_no_user_was_given(self):
        self.user_data['username'] = ''
        response = self.send_post()
        self.assertRedirects(response, reverse('todoapp:home'))

    def test_logout_view_redirects_to_home_if_given_user_is_different_to_request_user(self):
        self.user_data['username'] = 'joedoe'
        response = self.send_post()
        self.assertRedirects(response, reverse('todoapp:home'))

    def test_logout_view_is_logging_out_user_correctly(self):
        response = self.send_post(follow=True)
        content = response.content.decode('utf-8')
        self.assertIn(
            'You have been logged out successfully!',
            content
        )
