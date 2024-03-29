# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-02 18:00
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('event_scrapper', '0006_auto_20180819_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtlByDayEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('event_id', models.IntegerField(blank=True, null=True)),
                ('global_id', models.CharField(blank=True, max_length=500, null=True)),
                ('global_id_lineage', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('rest_url', models.CharField(blank=True, max_length=500, null=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('excerpt', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=500, null=True)),
                ('all_day', models.NullBooleanField(default=False)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('cost', models.CharField(blank=True, max_length=500, null=True)),
                ('website', models.CharField(blank=True, max_length=500, null=True)),
                ('json_ld', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AtlByDayOrganizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('organizer_id', models.IntegerField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('organizer', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=500, null=True)),
                ('phone', models.CharField(blank=True, max_length=500, null=True)),
                ('website', models.CharField(blank=True, max_length=500, null=True)),
                ('email', models.CharField(blank=True, max_length=500, null=True)),
                ('json_ld', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('global_id', models.CharField(blank=True, max_length=500, null=True)),
                ('global_id_lineage', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AtlByDayVenue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('venue_id', models.IntegerField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('venue', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=500, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.CharField(blank=True, max_length=500, null=True)),
                ('country', models.CharField(blank=True, max_length=500, null=True)),
                ('state', models.CharField(blank=True, max_length=500, null=True)),
                ('zip', models.CharField(blank=True, max_length=500, null=True)),
                ('phone', models.CharField(blank=True, max_length=500, null=True)),
                ('website', models.CharField(blank=True, max_length=500, null=True)),
                ('stateprovince', models.CharField(blank=True, max_length=500, null=True)),
                ('geo_lat', models.FloatField(blank=True, null=True)),
                ('geo_lng', models.FloatField(blank=True, null=True)),
                ('json_ld', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('global_id', models.CharField(blank=True, max_length=500, null=True)),
                ('global_id_lineage', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='atlbydayevent',
            name='organizer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event_scrapper.AtlByDayOrganizer'),
        ),
        migrations.AddField(
            model_name='atlbydayevent',
            name='venue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event_scrapper.AtlByDayVenue'),
        ),
    ]
