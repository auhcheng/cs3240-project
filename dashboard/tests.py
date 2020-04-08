from django.test import TestCase
from .views import get_weather_context, add_todo, complete_todo, delete_complete, delete_all, Dashboard

from .forms import TodoForm
from .models import Todo

from django.contrib.auth.models import User
from django.urls import reverse
from django.test.client import Client

class DashboardTests(TestCase):

    def test_weather_is_consistent(self):
        context1 = get_weather_context()
        context2 = get_weather_context()

        self.assertEqual(context1, context2)
    
    def test_weather_context_is_dict(self):
        context = get_weather_context()
        self.assertIsInstance(context, dict)
    
    def test_weather_city_is_Charlottesville(self):
        city_weather = get_weather_context()['city_weather']
        self.assertEqual(city_weather['city'], 'Charlottesville')
    
    def test_weather_temperature_is_number(self):
        city_weather = get_weather_context()['city_weather']
        self.assertIsInstance(city_weather['temperature'], float)
    
    def test_weather_description_is_string(self):
        city_weather = get_weather_context()['city_weather']
        self.assertIsInstance(city_weather['description'], str)

    # Below tests are for the todo model and task list functionality
    # database at the end directly affects the database itself with functionality used in the views
    # form at the end uses the views themselves

    # fills in task form with something
    def test_valid_todo_form(self):
        form = TodoForm({'task': "task"})
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.task, "task")
        task.user = "user"
        task = form.save()
        self.assertEqual(task.user, "user")

    # checks if blank form is valid
    def test_invalid_todo_form(self):
        form = TodoForm({'task': ""})
        self.assertFalse(form.is_valid())

    # adds task to database
    def test_add_task_database(self):
        task_count = Todo.objects.count()
        Todo.objects.create(task='test')
        tasks = Todo.objects.all()
        self.assertEqual(Todo.objects.count(), task_count + 1)

    # changes the value of a task to complete (based on logic from the complete_todo view)
    def test_complete_task_database(self):
        t = Todo.objects.create(task='test')
        t.complete = True
        t.save()
        self.assertTrue(Todo.objects.get(task='test').complete)
        t.complete = False
        t.save()
        self.assertFalse(Todo.objects.get(task='test').complete)

    # deletes a single task
    def test_delete_task_database(self):
        t = Todo.objects.create(task='test 1', user='te1st')
        num = t.id
        t = Todo.objects.create(task='test 2', user='te2st')
        task_count = Todo.objects.count();
        Todo.objects.filter(pk=num).delete()
        self.assertEqual(Todo.objects.count(), task_count - 1)

    # deletes all complete tasks for a user
    def test_delete_complete_database(self):
        Todo.objects.create(task='incomplete', user='te1st')
        t = Todo.objects.create(task='complete', user='te1st')
        t.complete = True
        t.save()
        Todo.objects.create(task='incomplete', user='te2st')
        t = Todo.objects.create(task='complete', user='te2st')
        t.complete = True
        t.save()
        task_count = Todo.objects.count()
        Todo.objects.filter(complete__exact=True, user__exact='te1st').delete()
        self.assertEqual(Todo.objects.count(), task_count - 1)

    # deletes all tasks for a user
    def test_delete_all_database(self):
        Todo.objects.create(task='test 1', user='te1st')
        Todo.objects.create(task='test 2', user='te2st')
        Todo.objects.create(task='test 3', user='te2st')
        task_count = Todo.objects.count()
        Todo.objects.filter(user__exact='te1st').delete()
        self.assertEqual(Todo.objects.count(), task_count - 1)