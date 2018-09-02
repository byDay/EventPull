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
from event_scrapper.atl_fetcher import AtlDataFetcher
from event_scrapper.atl_data_helper import DataHelper
from event_scrapper.serializers import EventSerializer
from event_scrapper.venue_scrapper import VenueScrapper

#Monthly Cron
@celery.decorators.periodic_task(run_every=crontab(day_of_month='1', hour=12, minute=00))
def trigger_scrapping_cron():
	all_venues = models.Venue.objects.filter(is_active=True)
	for venue in all_venues:
		process_venue_scrapping(venue.id)

@shared_task
def process_venue_scrapping(venue_id):
	venue = models.Venue.objects.get(id=venue_id)
	log = models.ScrapingEventLogs.objects.create(venue=venue, status=0, start_time=datetime.datetime.today())
	error_message = {}
	
	#Start Scraping
	try:
		venue_scrapper_obj = VenueScrapper(venue)
		event_obj_list = venue_scrapper_obj.scrape_venue()
		for event_obj in event_obj_list:
			serialized_event_data = EventSerializer(data=event_obj)
			if serialized_event_data.is_valid():
				serialized_event_data.save()
				status = 1
			else:
				status = 2
				error_message[event_obj['event_url']] = serialized_event_data.errors
	except Exception as e:
		status = 2
		error_message = str(e)

	#End Scraping
	log.end_time = datetime.datetime.today()
	log.status = status
	log.description = {'error_message' : error_message}
	log.save()


#Daily Cron
@periodic_task(run_every=crontab(minute=0, hour=8))
def pull_data_from_atlbyday_wordpress():

	atl_fetcher_obj = AtlDataFetcher()
	atl_data_helper_obj = DataHelper()
	
	#Fetch All Events
	all_events = atl_fetcher_obj.get_all_events()
	for event in all_events:
		atl_data_helper_obj.update_or_create_event(event)

	#Fetch All Venues
	all_venus = atl_fetcher_obj.get_all_venues()
	for venue in all_venus:
		atl_data_helper_obj.update_or_create_venue(event)

	#Fetch All Organizers
	all_orgainzer = atl_fetcher_obj.get_all_organizer()
	for organizer in all_orgainzer:
		atl_data_helper_obj.update_or_create_organizer(event)
