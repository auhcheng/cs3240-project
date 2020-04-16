# Generated by Django 3.0.3 on 2020-04-16 00:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_merge_20200415_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='todo',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 22, 17, 46, 37, 900802, tzinfo=utc)),
        ),
    ]