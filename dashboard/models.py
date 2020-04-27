from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import datetime
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    preferred_name = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Todo(models.Model):
    task = models.CharField(max_length=50, default="")
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due = models.DateTimeField(default=datetime.datetime(2020, 4, 22, 17, 46, 37, 900802, tzinfo=timezone.utc))
    current = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task

    def is_due(self):
        return self.current > self.due

class Note(models.Model):
    title = models.CharField(max_length=50, default="")
    body = models.TextField(max_length=5000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def archive(self):
        is_archived = True

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a class="pl-2" href="{url}"> {self.title} </a>'