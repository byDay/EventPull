# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-19 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_scrapper', '0003_auto_20180819_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
