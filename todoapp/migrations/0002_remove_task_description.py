# Generated by Django 5.0 on 2024-02-11 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
    ]
