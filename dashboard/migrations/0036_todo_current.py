# Generated by Django 3.0.3 on 2020-04-27 00:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_auto_20200426_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='current',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
