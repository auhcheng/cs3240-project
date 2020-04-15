from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from dashboard.models import Profile, Todo, Note, Event
from django import forms
from .widgets import BootstrapDateTimePickerInput


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')


class TodoFormText(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('task',)


class TodoFormDate(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('due',)


class TodoFormTextDate(forms.ModelForm):
    due = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput(format='%d/%m/%Y %H:%M')
    )
    class Meta:
        model = Todo
        fields = ('task', 'due',)
        widgets = {
            'task': forms.TextInput(attrs={'placeholder': 'New task', 'class': 'form-control'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'body')

class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput(format='%d/%m/%Y %H:%M')
    )
    end_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput(format='%d/%m/%Y %H:%M')
    )

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
