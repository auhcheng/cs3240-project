from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile, Todo
from .forms import UserForm, ProfileForm, TodoFormText, TodoFormDate, TodoFormTextDate
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

        # read the form data from the POST request into a TodoFormText
        todo_form = TodoFormTextDate(request.POST)
        if todo_form.is_valid():

            # get the Todo instance from the TodoFormText without saving
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
        todo_form = TodoFormTextDate()

        # render everything as normal
        context = get_weather_context()
        context['todo_list'] = Todo.objects.order_by('id')
        context['todo_form'] = todo_form
        return render(request, 'dashboard/dashboard.html', context)


@login_required
def TaskPage(request, todo_id):
    if request.method == 'POST':
        todo_form_text = TodoFormText(request.POST)
        todo_form_date = TodoFormDate(request.POST)
        if todo_form_text.is_valid():  # valid data
            # update todo in question
            todo = Todo.objects.get(pk=todo_id)
            todo_form_text = TodoFormText(request.POST, instance=todo)
            todo_form_text.save()

            # defaults and returns to original page
            todo_form_text = TodoFormText()
            todo_form_date = TodoFormDate()
            context = {'todo_form_text': todo_form_text, 'todo_form_date': todo_form_date, 'todo': Todo.objects.get(pk=todo_id), 'update': "Updated task name!"}
            return render(request, 'dashboard/todo.html', context)
        elif todo_form_date.is_valid():
            todo = Todo.objects.get(pk=todo_id)
            todo_form_date = TodoFormDate(request.POST, instance=todo)
            todo_form_date.save()

            # defaults and returns to original page
            todo_form_text = TodoFormText()
            todo_form_date = TodoFormDate()
            context = {'todo_form_text': todo_form_text, 'todo_form_date': todo_form_date, 'todo': Todo.objects.get(pk=todo_id), 'update': "Updated due date!"}
            return render(request, 'dashboard/todo.html', context)
        else:
            # defaults and returns to original page
            todo_form_text = TodoFormText()
            todo_form_date = TodoFormDate()
            context = {'todo_form_text': todo_form_text, 'todo_form_date': todo_form_date, 'todo': Todo.objects.get(pk=todo_id), 'update': "Nothing was updated."}
            return render(request, 'dashboard/todo.html', context)
    else:  # GET request
        todo_form_text = TodoFormText()
        todo_form_date = TodoFormDate()
        context = {'todo_form_text': todo_form_text, 'todo_form_date': todo_form_date, 'todo': Todo.objects.get(pk=todo_id), 'update': ""}
        return render(request, 'dashboard/todo.html', context)


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
        todo_form = TodoFormText(request.POST)
        if todo_form.is_valid():
            temp_todo = todo_form.save(commit=False)
            temp_todo.user = request.user
            temp_todo.save()
            todo_form.save_m2m()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, ('Please correct the error.'))
    # else:
    #     todo_form = TodoFormText(instance=request.user.todo)
    context = get_weather_context()
    context['todo_list'] = Todo.objects.order_by('id')
    context['todo_form'] = TodoFormTextDate()
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def complete_todo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if todo.complete:
        todo.complete = False
        update = "Now incomplete!"
    else:
        todo.complete = True
        update = "Now complete!"
    todo.save()

    todo_form_text = TodoFormText()
    context = {'todo_form_text': todo_form_text, 'todo': Todo.objects.get(pk=todo_id), 'update': update}
    return render(request, 'dashboard/todo.html', context)


@login_required
def delete(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.delete()
    return redirect("dashboard")


@login_required
def delete_complete(request):
    Todo.objects.filter(complete__exact=True, user__exact=request.user).delete()
    return redirect("dashboard")


@login_required
def delete_all(request):
    Todo.objects.filter(user__exact=request.user).delete()
    return redirect("dashboard")


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')
