from django.contrib import admin

# Register your models here.
from .models import Todo, Event
admin.site.register(Todo)
admin.site.register(Event)