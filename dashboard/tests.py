from django.test import TestCase
from .views import get_weather_context

from .forms import TodoForm
from .models import Todo

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

class DashboardTests(TestCase):

    def test_weather_is_consistent(self):
        context1 = get_weather_context()
        context2 = get_weather_context()

        self.assertEqual(context1, context2)

    def test_valid_form(self):
        form = TodoForm({'task': "task"})
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.task, "task")
        task.user = "user"
        task = form.save()
        self.assertEqual(task.user, "user")

    def test_blank_form(self):
        form = TodoForm({})
        self.assertFalse(form.is_valid())

    def test_add_task(self):
        client = Client()
        client.login(username='mst3k@virginia.edu', password='password')
        res