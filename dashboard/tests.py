from django.test import TestCase
from .views import get_weather_context, add_todo, complete_todo, delete_complete, delete_all, Dashboard

from .forms import TodoForm
from .models import Todo, Event
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
        form = TodoForm({'task': "task", "due": "05/01/2020 12:00"})
        self.assertTrue(form.is_valid())
        task = form.save(commit=False)
        user = User(username='testuser'); user.save()
        task.user = user
        task.save()
        self.assertEqual(task.task, "task")
        self.assertEqual(task.user, user)

    # checks if updating a task's text works
    def test_valid_todo_text_form(self):
        form = TodoForm({'task': "task", "due": "05/01/2020 12:00"})
        self.assertTrue(form.is_valid())
        task = form.save(commit=False)
        user = User(username='testuser'); user.save()
        task.user = user
        task.save()
        text_form = TodoForm({'task': "altered task", "due": "05/01/2020 12:00"}, instance=task)
        text_form.save()
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
        form = TodoForm({'task': "", "due": "05/01/2020 12:00"})
        self.assertFalse(form.is_valid())
        form = TodoForm({'task': "test", "due": ""})
        self.assertFalse(form.is_valid())

    # checks if blank form is valid
    def test_invalid_todo_text_form(self):
        form = TodoForm({'task': ""})
        self.assertFalse(form.is_valid())

    # checks if blank form is valid
    def test_invalid_todo_date_form(self):
        form = TodoForm({"due": ""})
        self.assertFalse(form.is_valid())

    # adds task to database
    def test_add_task_database(self):
        user = User(username='testuser'); user.save()
        task_count = Todo.objects.count()
        Todo.objects.create(task='test', user=user)
        tasks = Todo.objects.all()
        self.assertEqual(Todo.objects.count(), task_count + 1)

    # changes the value of a task to complete (based on logic from the complete_todo view)
    def test_complete_task_database(self):
        user = User(username='testuser'); user.save()
        t = Todo.objects.create(task='test', user=user)
        t.complete = True
        t.save()
        self.assertTrue(Todo.objects.get(task='test').complete)
        t.complete = False
        t.save()
        self.assertFalse(Todo.objects.get(task='test').complete)

    # deletes a single task
    def test_delete_task_database(self):
        user1 = User(username='testuser1'); user1.save()
        user2 = User(username='testuser2'); user2.save()
        t = Todo.objects.create(task='test 1', user=user1)
        num = t.id
        t = Todo.objects.create(task='test 2', user=user2)
        task_count = Todo.objects.count()
        Todo.objects.filter(pk=num).delete()
        self.assertEqual(Todo.objects.count(), task_count - 1)

    # deletes all complete tasks for a user
    def test_delete_complete_database(self):
        user1 = User(username='testuser1'); user1.save()
        user2 = User(username='testuser2'); user2.save()
        Todo.objects.create(task='incomplete', user=user1)
        t = Todo.objects.create(task='complete', user=user1)
        t.complete = True
        t.save()
        Todo.objects.create(task='incomplete', user=user2)
        t = Todo.objects.create(task='complete', user=user2)
        t.complete = True
        t.save()
        task_count = Todo.objects.count()
        Todo.objects.filter(complete__exact=True, user__exact=user1).delete()
        self.assertEqual(Todo.objects.count(), task_count - 1)

    # deletes all tasks for a user
    def test_delete_all_database(self):
        user1 = User(username='testuser1'); user1.save()
        user2 = User(username='testuser2'); user2.save()
        Todo.objects.create(task='test 1', user=user1)
        Todo.objects.create(task='test 2', user=user2)
        Todo.objects.create(task='test 3', user=user2)
        task_count = Todo.objects.count()
        Todo.objects.filter(user__exact=user1).delete()
        self.assertEqual(Todo.objects.count(), task_count - 1)

    def test_login(self):
        c = Client()
        user = User(username='testuser')
        user.save()
        not_logged_in = c.get('/')

        # we should be redirected
        self.assertEqual(not_logged_in.status_code, 302) # 302 means redirect
        self.assertEqual(not_logged_in.url, '/account/login/?next=/')
        
        c.force_login(user)
        logged_in = c.get('/dashboard/')
        self.assertEqual(logged_in.status_code, 200) # 200 means success
    
    def test_events_are_private(self):
        user1 = User(username='testuser1'); user1.save()
        user2 = User(username='testuser2'); user2.save()
        e = Event.objects.create(title='', description='', start_time=datetime.datetime.now(), end_time=datetime.datetime.now(), user=user1)
        event_id = e.pk
        e.save()

        c1 = Client()
        c1.force_login(user1)
        try_to_edit = c1.get(reverse('event_edit', args=(event_id,)))
        self.assertEqual(try_to_edit.status_code, 200)

        c2 = Client()
        c2.force_login(user2)
        try_to_edit = c2.get(reverse('event_edit', args=(event_id,)))
        self.assertEqual(try_to_edit.status_code, 404)