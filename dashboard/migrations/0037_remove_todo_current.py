# Generated by Django 3.0.3 on 2020-04-27 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_todo_current'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='current',
        ),
    ]