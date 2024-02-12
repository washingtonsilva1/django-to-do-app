import string
from random import SystemRandom

from django.contrib.auth.models import User
from todoapp.models import Task


class TaskMixin:
    def create_user(self, username='dummyuser', password='#JoeDoe21'):
        return User.objects.create_user(
            username=username,
            password=password
        )

    def create_task(self,
                    name='Task Example',
                    is_completed=False,
                    user=None):
        if user is None:
            user = self.create_user()
        return Task.objects.create(
            name=name,
            is_completed=is_completed,
            user=user
        )

    def create_task_sample(self, n=5, user=None):
        if user is None:
            user = self.create_user()
        tasks = []
        for i in range(1, n+1):
            tasks.append(self.create_task(
                name=f'Task #{i}',
                user=user
            ))
        tasks.reverse()
        return tasks


def generate_random_string(n=5):
    p = string.ascii_letters + string.digits
    return ''.join(SystemRandom().choices(p, k=n))
