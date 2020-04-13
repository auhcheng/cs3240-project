from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User,unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
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
    user = models.CharField(max_length=6, default="")
    due = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=7))  # a week from now

    def __str__(self):
        return self.task
