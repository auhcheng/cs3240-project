from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile, Todo
from .forms import UserForm,ProfileForm, TodoForm
from django.views.decorators.http import require_POST
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
    context = get_weather_context()
    context['todo_list'] = Todo.objects.order_by('id')
    # context['todo_form'] = TodoForm()
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
@require_POST
def add_todo(request):
    todo_form = TodoForm(request.POST)
    print(request.POST['task'])
    return HttpResponseRedirect('dashboard.dashboard.html')


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')