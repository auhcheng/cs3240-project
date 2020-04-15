from django.test import TestCase
from .views import get_weather_context, add_todo, complete_todo, delete_complete, delete_all, Dashboard

from .forms import TodoFormTextDate, TodoFormDate, TodoFormText
from .models import Todo
import datetime, pytz
from django.utils import timezone

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
    # database/form at the end directly affects the database itself with functionality used in the views
    # view at the end uses the views themselves

    # fills in task form with something
    def test_valid_todo_textdate_form(self):
        form = TodoFormTextDate({'task': "task", "due": "05/01/2020 12:00"})
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.task, "task")
        task.user = "user"
        task = form.save()
        self.assertEqual(task.user, "user")

    # checks if updating a task's text works
    def test_valid_todo_text_form(self):
        form = TodoFormTextDate({'task': "task", "due": "05/01/2020 12:00"})
        self.assertTrue(form.is_valid())
        task = form.save()
        text_form = TodoFormText({'task':"altered task"}, instance=task)
        text_form.save();
        self.assertEqual(task.task, "altered task")

    # # checks if updating a task's due date works
    # def test_valid_todo_date_form(self):
    #     form = TodoFormTextDate({'task': "task", "due": "05/01/2020 12:00"})
    #     self.assertTrue(form.is_valid())
    #     task = form.save()
    #     date_form = TodoFormDate({"due": "05/08/2020 12:00"}, instance=task)
    #     date_form.save()
    #     test_datetime = datetime.datetime(year=2020, month=5, day=8, hour=12, minute=0)
    #     timezone.make_aware(test_datetime)
    #
    #     self.assertEqual(task.due, test_datetime)

    # checks if blank form is valid
    def test_invalid_todo_textdate_form(self):
        form = TodoFormTextDate({'task': "", "due": "05/01/2020 12:00"})
        self.assertFalse(form.is_valid())
        form = TodoFormTextDate({'task': "test", "due": ""})
        self.assertFalse(form.is_valid())

    # checks if blank form is valid
    def test_invalid_todo_text_form(self):
        form = TodoFormText({'task': ""})
        self.assertFalse(form.is_valid())

    # checks if blank form is valid
    def test_invalid_todo_date_form(self):
        form = TodoFormDate({"due": ""})
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
