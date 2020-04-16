from __future__ import print_function
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile, Todo, Note
from .forms import ProfileForm, TodoForm, NoteForm
from django.contrib import messages
import requests
from django.utils import timezone

import datetime
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from .models import *
from .utils import Calendar
from .forms import EventForm

class CalendarView(generic.ListView):
    model = Event
    template_name = 'dashboard/calendar.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'dashboard/event.html', {'form': form})

@login_required
def edit_todo(request, todo_id=None):
    instance = get_object_or_404(Todo, pk=todo_id)

    form = TodoForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('todolist'))
    
    return render(request, 'dashboard/todo.html', {'form': form})

def get_weather_context(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c163a4ad293113133fd9322210f18836'
    
    try:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
    except KeyError:
        city = "Charlottesville"
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
    

    context = {'city_weather': city_weather}
    return context


@login_required
def Dashboard(request):
    # if the form has been filled out and sent to us as a POST request
    if request.method == 'POST':
        return HttpResponseRedirect("/")
    else:
        # we are getting this page as a GET request        
        # render everything as normal
        city = request.user.profile.city_location
        context = get_weather_context(city)
        return render(request, 'dashboard/dashboard.html', context)


@login_required
def TodosPage(request):
    context=dict()
    # if the form has been filled out and sent to us as a POST request
    if request.method == 'POST':

        # read the form data from the POST request into a TodoFormText
        todo_form = TodoForm(request.POST)

        if todo_form.is_valid():
            # get the Todo instance from the TodoFormText without saving
            todo = todo_form.save(commit=False)

            # set the user of this Todo to the current user
            todo.user = request.user

            todo.save()
            return HttpResponseRedirect('/todos')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        # we are getting this page as a GET request

        # create a blank form
        todo_form = TodoForm()      
        # render everything as normal
        context['todo_list'] = Todo.objects.order_by('id')
        context['todo_form'] = todo_form          
        return render(request, 'dashboard/todolist.html', context)

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'dashboard/profile.html', {
        'profile_form': profile_form
    })


@login_required
def NotesPage(request):
# if the form has been filled out and sent to us as a POST request
    context = {}
    if request.method == 'POST':
        # read the form data from the POST request into a TodoFormText        
        note_form = NoteForm(request.POST)        
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.user = request.user
            note.save()
            return HttpResponseRedirect('/notes')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        # we are getting this page as a GET request

        # render everything as normal                
        context['note_list'] = Note.objects.order_by('id')
        context['note_form'] = NoteForm()   
        return render(request, 'dashboard/note.html', context)


def ArchivePage(request):
    context = {'note_list': Note.objects.order_by('id')}
    return render(request, 'dashboard/notearchive.html', context)


@login_required
def add_todo(request):
    context = {}
    if request.method == 'POST':
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid():
            temp_todo = todo_form.save(commit=False)
            temp_todo.user = request.user
            temp_todo.save()
            todo_form.save_m2m()
            return HttpResponseRedirect('/todos')
        else:
            messages.error(request, ('Please correct the error.'))    
    else:
        context['todo_list'] = Todo.objects.order_by('id')
        context['todo_form'] = TodoForm()
        return render(request, 'dashboard/todolist.html', context)

@login_required
def complete_todo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = not todo.complete
    todo.save()

    return redirect("/todos")


@login_required
def delete(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.delete()
    return redirect("/todos")


@login_required
def delete_complete(request):
    Todo.objects.filter(complete__exact=True, user__exact=request.user).delete()
    return redirect("/todos")


@login_required
def delete_all(request):
    Todo.objects.filter(user__exact=request.user).delete()
    return redirect("/todos")


@login_required
def delete_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect("/notes")


@login_required
def delete_note_archive(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect("/archive")


@login_required
def delete_note_all(request):
    Note.objects.filter(user__exact=request.user, is_archived=False).delete()
    return redirect("/notes")


@login_required
def delete_note_archive_all(request):
    Note.objects.filter(user__exact=request.user, is_archived=True).delete()
    return redirect("/archive")


@login_required
def archive_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.is_archived = True
    note.save()
    return redirect("/notes")


@login_required
def unarchive_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.is_archived = False
    note.save()
    return redirect("/archive")


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')