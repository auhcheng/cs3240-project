from __future__ import print_function
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile, Todo, Note
from .forms import ProfileForm, TodoForm, NoteForm, SearchForm
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
from django.http import HttpResponseNotFound
import geocoder


class CalendarView(generic.ListView):
    model = Event
    template_name = 'dashboard/calendar.html'

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(events=self.get_queryset(), withyear=True)
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
        if instance.user != request.user:
            return HttpResponseNotFound("You don't have access to this event.")
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
    
    return render(request, 'dashboard/todo.html', {'form': form, 'todo': instance})

def get_charlottesville_weather_context():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&units=imperial&appid=c163a4ad293113133fd9322210f18836'
    r = requests.get(url.format('Charlottesville', 'Virginia')).json()
    city_weather = {
                'city': 'Charlottesville',
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }
    context = {'city_weather': city_weather, 'city_found': False}
    return context

def get_weather_context():
    try:
        g = geocoder.ip('me')
        lat, lng = g.latlng
        url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=imperial&appid=c163a4ad293113133fd9322210f18836'
        r = requests.get(url.format(lat, lng)).json()
        city_weather = {
                    'city': r['name'],
                    'temperature': r['main']['temp'],
                    'description': r['weather'][0]['description'],
                    'icon': r['weather'][0]['icon'],
                }
        
        context = {'city_weather': city_weather, 'city_found': True}
        return context
    except:
        return get_charlottesville_weather_context()


@login_required
def Dashboard(request):
    # if the form has been filled out and sent to us as a POST request
    if request.method == 'POST':
        # read the form data from the POST request into a TodoFormText        
        note_form = NoteForm(request.POST)        
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.user = request.user
            note.save()
            return HttpResponseRedirect('/dashboard')            
        else:
            messages.error(request, ('Please correct the error below.'))        
    else:
        # we are getting this page as a GET request        
        # render everything as normal        
        context = get_weather_context()
        context['note_list'] = Note.objects.order_by('id')
        context['note_form'] = NoteForm()   
        return render(request, 'dashboard/dashboard.html', context)

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
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            context['search_term'] = search_form.cleaned_data['search']

        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.user = request.user
            note.save()

        else:
            messages.error(request, 'Please correct the error below.')

        # render everything as normal
        context['note_list'] = Note.objects.order_by('id')
        context['note_form'] = NoteForm()
        context['search_form'] = SearchForm(request.POST)
        return render(request, 'dashboard/note.html', context)

    else:
        # we are getting this page as a GET request

        # render everything as normal                
        context['note_list'] = Note.objects.order_by('id')
        context['note_form'] = NoteForm()
        context['search_form'] = SearchForm()
        context['search_term'] = ''
        return render(request, 'dashboard/note.html', context)

@login_required
def delete_note(request, note_id, redir):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect(redir)


@login_required
def delete_note_archive(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect("/archive")


@login_required
def delete_note_all(request, redir):
    Note.objects.filter(user__exact=request.user, is_archived=False).delete()
    return redirect(redir)


@login_required
def delete_note_archive_all(request):
    Note.objects.filter(user__exact=request.user, is_archived=True).delete()
    return redirect("/archive")


@login_required
def archive_note(request, note_id, redir):
    note = Note.objects.get(pk=note_id)
    note.is_archived = True
    note.save()
    return redirect(redir)


@login_required
def unarchive_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.is_archived = False
    note.save()
    return redirect("/archive")

def ArchivePage(request):
    context = {'note_list': Note.objects.order_by('id')}
    return render(request, 'dashboard/notearchive.html', context)

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

            # updates due date stuff
            for todo in Todo.objects.all():
                todo.current = timezone.localtime(timezone.now()+datetime.timedelta(hours=1))
                todo.save()


            return HttpResponseRedirect('/todos')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        # we are getting this page as a GET request

        # updates due date stuff
        for todo in Todo.objects.all():
            todo.current = timezone.localtime(timezone.now()+datetime.timedelta(hours=1))
            todo.save()

        # create a blank form
        todo_form = TodoForm()      
        # render everything as normal
        context['todo_list'] = Todo.objects.order_by('id')
        context['todo_list_due'] = Todo.objects.order_by('due')
        context['todo_form'] = todo_form          
        return render(request, 'dashboard/todolist.html', context)


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


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')