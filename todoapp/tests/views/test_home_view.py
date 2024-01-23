from todoapp.views import HomeTemplateView
from utils.utils import TaskMixin

from unittest.mock import patch
from django.test import TestCase
from django.urls import resolve, reverse


class HomeViewTest(TestCase, TaskMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': '#DummyPassword'
        }
        self.user = self.create_user(
            self.user_data['username'],
            self.user_data['password']
        )
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password']
        )

    def test_home_view_is_using_correct_view_class(self):
        view = resolve(reverse('todoapp:home'))
        self.assertIs(view.func.view_class, HomeTemplateView)

    def test_home_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('todoapp:home'))
        self.assertTemplateUsed(response, 'todoapp/view/home.html')

    def test_home_view_title_is_rendering_correctly(self):
        response = self.client.get(reverse('todoapp:home'))
        title_needed = f'{response.context["title"]} | ToDo - App'
        content = response.content.decode('utf-8')
        self.assertIn(title_needed, content)

    def test_home_view_display_default_text_if_does_not_have_any_task(self):
        response = self.client.get(reverse('todoapp:home'))
        text_needed = 'No tasks were found'
        content = response.content.decode('utf-8')
        self.assertIn(text_needed, content)

    def test_home_view_is_displaying_tasks(self):
        task_needed = 'This is what i am looking for'

        self.create_task(name=task_needed, user=self.user)
        response = self.client.get(reverse('todoapp:home'))
        content = response.content.decode('utf-8')
        self.assertIn(task_needed, content)

    def test_home_view_does_not_display_other_users_tasks(self):
        this_task_is_mine = 'First task'
        this_task_is_not_mine = 'Second task'

        self.create_task(name=this_task_is_mine, user=self.user)
        self.create_task(name=this_task_is_not_mine)
        response = self.client.get(reverse('todoapp:home'))
        content = response.content.decode('utf-8')
        self.assertIn(this_task_is_mine, content)
        self.assertNotIn(this_task_is_not_mine, content)

    def test_home_view_pending_tasks_got_task_pending_class(self):
        self.create_task(is_completed=False, user=self.user)
        response = self.client.get(reverse('todoapp:home'))
        content = response.content.decode('utf-8')
        self.assertIn('task-pending', content)

    def test_home_view_completed_tasks_got_task_completed_class(self):
        self.create_task(is_completed=True, user=self.user)
        response = self.client.get(reverse('todoapp:home'))
        content = response.content.decode('utf-8')
        self.assertIn('task-completed', content)

    @patch('django.conf.settings.OBJECTS_PER_PAGE', new=15)
    def test_home_view_tasks_are_displayed_according_to_settings_config(self):
        tasks = self.create_task_sample(n=20, user=self.user)
        response = self.client.get(reverse('todoapp:home'))
        self.assertEqual(
            tasks[:15],
            response.context['page'].object_list
        )
        second_page = list(
            response.context['page'].paginator.get_page(2).object_list
        )
        self.assertEqual(tasks[15:], second_page)

    def test_home_view_searching_for_a_task_by_name_or_description(self):
        search_term = 'That is waht i am looking for'

        task = self.create_task(name=search_term, user=self.user)
        self.create_task_sample(user=self.user)
        response = self.client.get(
            reverse('todoapp:home'),
            data={
                'q': search_term
            }
        )
        self.assertIn(task, response.context['page'].object_list)
        self.assertEqual(1, len(response.context['page'].object_list))
