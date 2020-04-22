from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from dashboard.models import Profile, Todo, Note, Event
from django import forms
from .widgets import BootstrapDateTimePickerInput


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('preferred_name',)
        widgets = {
            'preferred_name': forms.TextInput(attrs={'placeholder': 'Preferred name', 'class': 'form-control'}),
        }

class TodoForm(forms.ModelForm):
    due = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M', '%m/%d/%Y %I:%M %p'],
        widget=BootstrapDateTimePickerInput(format='%d/%m/%Y %H:%M', attrs={'placeholder': 'Deadline'})
    )
    class Meta:
        model = Todo
        fields = ('task', 'due')
        widgets = {
            'task': forms.TextInput(attrs={'placeholder': 'New task', 'class': 'form-control'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'body')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New note'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Body',
                                        'style': 'height: 10rem'}),
        }

class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M', '%m/%d/%Y %I:%M %p'],
        widget=BootstrapDateTimePickerInput(format='%d/%m/%Y %H:%M')
    )
    end_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M', '%m/%d/%Y %I:%M %p'],
        widget=BootstrapDateTimePickerInput(format='%d/%m/%Y %H:%M')
    )

    class Meta:
        model = Event
        fields = ('title', 'description', 'start_time', 'end_time')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
