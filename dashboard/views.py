from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile, Todo
from .forms import UserForm,ProfileForm, TodoForm
from django.contrib import messages
import requests

def get_weather_context():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c163a4ad293113133fd9322210f18836'
    city = 'Charlottesville'

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

        # read the form data from the POST request into a TodoForm
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid():

            # get the Todo instance from the TodoForm without saving
            todo = todo_form.save(commit=False)

            # set the user of this Todo to the current user
            todo.user = request.user

            todo.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        # we are getting this page as a GET request

        # create a blank form
        todo_form = TodoForm()

        # render everything as normal
        context = get_weather_context()
        context['todo_list'] = Todo.objects.order_by('id')
        context['todo_form'] = TodoForm()
        return render(request, 'dashboard/dashboard.html', context)

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'dashboard/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def add_todo(request):
    if request.method == 'POST':
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid():
            temp_todo = todo_form.save(commit=False)
            temp_todo.user = request.user
            temp_todo.save()
            todo_form.save_m2m()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, ('Please correct the error.'))
    else:
        todo_form = TodoForm(instance=request.user.todo)
    context = get_weather_context()
    context['todo_list'] = Todo.objects.order_by('id')
    context['todo_form'] = TodoForm()
    return render(request, 'dashboard/dashboard.html', context)


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')