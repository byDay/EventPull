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
	venue_metadata = JSONField(null=True, blank=True)

	def __str__(self):
		return str(self.name)


class Event(TimeStampedModel):

	name = models.CharField(max_length=255, null=False, blank=False)
	event_id = models.CharField(max_length=255, null=True, blank=True)
	description = models.CharField(max_length=10000, null=True, blank=True)
	start_date = models.DateField(null=False)
	event_start_time = models.DateTimeField(null=True)
	end_date = models.DateField(null=False)
	event_end_time = models.DateTimeField(null=True)
	tags = JSONField(null=True, blank=True)
	is_all_day_event = models.NullBooleanField(null=True, blank=True, default=False)
	venue = models.ForeignKey(Venue, null=False)
	category = models.CharField(max_length=255, null=True, blank=True)
	event_url = models.CharField(max_length=255, null=True, blank=True)
	organizer_name = models.CharField(max_length=255, null=True, blank=True)
	organizer_url = models.CharField(max_length=255, null=True, blank=True)
	minimum_cost = models.CharField(max_length=255, null=True, blank=True)
	event_metadata = JSONField(null=True, blank=True)

	def __str__(self):
		return str(self.venue.name) + '-' + str(self.name) + '-' + str(self.start_date)


class Config(TimeStampedModel):

	name = models.CharField(max_length=10000, null=False, blank=False)
	config = JSONField(null=False)


class ScrapingEventLogs(TimeStampedModel):

	status_choices = Choices(
		(0, 'In Progress'),
		(1, 'Success'),
		(2, 'Failed'),
	)
	
	status = models.IntegerField(choices=status_choices, null=False)
	venue = models.ForeignKey(Venue, null=False)
	start_time = models.DateTimeField(null=True)
	end_time = models.DateTimeField(null=True)
	description = JSONField(null=True, blank=True)


class AtlByDayVenue(TimeStampedModel):
	venue_id = models.IntegerField(null=True, blank=True)
	author = models.CharField(max_length=10000, null=True, blank=True)
	status = models.CharField(max_length=10000, null=True, blank=True)
	url = models.CharField(max_length=10000, null=True, blank=True)
	venue = models.CharField(max_length=10000, null=True, blank=True)
	slug = models.CharField(max_length=10000, null=True, blank=True)
	address = models.CharField(max_length=10000, null=True, blank=True)
	city = models.CharField(max_length=10000, null=True, blank=True)
	country = models.CharField(max_length=10000, null=True, blank=True)
	state = models.CharField(max_length=10000, null=True, blank=True)
	zip = models.CharField(max_length=10000, null=True, blank=True)
	phone = models.CharField(max_length=10000, null=True, blank=True)
	website = models.CharField(max_length=10000, null=True, blank=True)
	stateprovince = models.CharField(max_length=10000, null=True, blank=True)
	geo_lat = models.FloatField(null=True, blank=True)
	geo_lng = models.FloatField(null=True, blank=True)
	json_ld = JSONField(null=True, blank=True)
	global_id = models.CharField(max_length=10000, null=True, blank=True)
	global_id_lineage = JSONField(null=True, blank=True)

	def __unicode__(self):
		return str(self.venue) if self.venue else str(self.venue_id)


class AtlByDayOrganizer(TimeStampedModel):
	organizer_id = models.IntegerField(null=True, blank=True)
	author = models.CharField(max_length=10000, null=True, blank=True)
	status = models.CharField(max_length=10000, null=True, blank=True)
	url = models.CharField(max_length=10000, null=True, blank=True)
	organizer = models.CharField(max_length=10000, null=True, blank=True)
	slug = models.CharField(max_length=10000, null=True, blank=True)
	phone = models.CharField(max_length=10000, null=True, blank=True)
	website =models.CharField(max_length=10000, null=True, blank=True)
	email = models.CharField(max_length=10000, null=True, blank=True)
	json_ld = JSONField(null=True, blank=True)
	global_id = models.CharField(max_length=10000, null=True, blank=True)
	global_id_lineage = JSONField(null=True, blank=True)

	def __unicode__(self):
		return str(self.organizer) if self.organizer else str(self.organizer_id)


class AtlByDayEvent(TimeStampedModel):
	event_id = models.IntegerField(null=True, blank=True)
	global_id = models.CharField(max_length=10000, null=True, blank=True)
	global_id_lineage = JSONField(null=True, blank=True)
	author = models.CharField(max_length=10000, null=True, blank=True)
	status = models.CharField(max_length=10000, null=True, blank=True)
	url = models.CharField(max_length=10000, null=True, blank=True)
	rest_url = models.CharField(max_length=10000, null=True, blank=True)
	title = models.CharField(max_length=10000, null=True, blank=True)
	description = models.CharField(max_length=10000, null=True, blank=True)
	excerpt = models.CharField(max_length=10000, null=True, blank=True)
	slug = models.CharField(max_length=10000, null=True, blank=True)
	all_day = models.NullBooleanField(null=True, blank=True, default=False)
	start_date = models.DateTimeField(null=True)
	end_date = models.DateTimeField(null=True)
	cost = models.CharField(max_length=10000, null=True, blank=True)
	website = models.CharField(max_length=10000, null=True, blank=True)
	venue = models.ForeignKey(AtlByDayVenue, null=True)
	organizer = models.ForeignKey(AtlByDayOrganizer, null=True)
	json_ld = JSONField(null=True, blank=True)

	def __unicode__(self):
		return str(self.title) if self.title else str(self.event_id)