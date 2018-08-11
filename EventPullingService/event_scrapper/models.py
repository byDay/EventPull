from __future__ import unicode_literals

from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField


class Venue(TimeStampedModel):

    name = models.CharField(max_length=255, null=False, blank=False)
    url_config = JSONField(null=False)
    scraping_config = JSONField(null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class Event(TimeStampedModel):

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.IntegerField(max_length=500, null=True, blank=True)
    date = models.DateField(null=False)
    event_start_time = models.DateTimeField(null=True)
    event_end_time = models.DateTimeField(null=True)
    tags = JSONField(null=True)
    venue = models.ForeignKey(Venue, null=False)

    def __str__(self):
        return str(self.venue.name) + '-' + str(self.name) + '-' + str(self.date)


class Config(TimeStampedModel):

	name = models.CharField(max_length=500, null=False, blank=False)
	config = JSONField(null=False)


class ScrapingEventLogs(TimeStampedModel):

	status_choices = Choices(
        (0, 'In Progress'),
        (1, 'Success'),
        (2, 'Failed'),
    )

	status = models.IntegerField(choices=status_choices, null=False)
	start_time = models.DateTimeField(null=True)
	end_time = models.DateTimeField(null=True)
	description = JSONField(null=True)