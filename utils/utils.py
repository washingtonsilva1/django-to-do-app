from django.contrib.auth.models import User


def create_user(username='dummyuser', password='#JoeDoe21'):
    return User.objects.create_user(
        username=username,
        password=password
    )
