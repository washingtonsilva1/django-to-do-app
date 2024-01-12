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
                    desc='Task Description',
                    is_completed=False,
                    user=None):
        if user is None:
            user = self.create_user()
        return Task.objects.create(
            name=name,
            description=desc,
            is_completed=is_completed,
            user=user
        )
