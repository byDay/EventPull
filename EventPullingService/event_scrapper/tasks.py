from __future__ import absolute_import

import time
import celery
import requests
import datetime
from bs4 import BeautifulSoup
from celery import shared_task
from event_scrapper import models
from celery.schedules import crontab
from celery.decorators import task, periodic_task
from event_scrapper.serializers import EventSerializer
from event_scrapper.venue_scrapper import VenueScrapper

#Monthly Cron
#@celery.decorators.periodic_task(run_every=crontab(minute='1'))
def trigger_scrapping_cron():
	all_venues = models.Venue.objects.filter(is_active=True)
	for venue in all_venues:
		process_venue_scrapping(venue)

def process_venue_scrapping(venue):
	log = models.ScrapingEventLogs.objects.create(venue=venue, status=0, start_time=datetime.datetime.today())
	error_message = None
	
	#Start Scraping
	# try:
	venue_scrapper_obj = VenueScrapper(venue)
	event_obj_list = venue_scrapper_obj.scrape_venue()
	serialized_event_data = EventSerializer(data=event_obj_list, many=True)
	if serialized_event_data.is_valid():
		serialized_event_data.save()
		status = 1
	else:
		status = 2
		error_message = serialized_event_data.errors
	# except Exception as e:
	# 	status = 2
	# 	error_message = str(e)

	#End Scraping
	log.end_time = datetime.datetime.today()
	log.status = status
	log.description = {'error_message' : error_message}
	log.save()
