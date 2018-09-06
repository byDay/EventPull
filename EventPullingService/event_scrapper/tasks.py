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
from event_scrapper.atl_data_helper import WPDataHelper
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
				event_obj['venue'] = {"id" : venue.venue_metadata.get('atl_venue_id')}
				created = WPDataHelper.create_wp_event(event_obj)
				if created:
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

	event_pull_log_obj = models.AtlPullEventLogs.objects.create(status=0, start_time=datetime.datetime.today())

	try:
		atl_fetcher_obj = AtlDataFetcher()
		atl_data_helper_obj = DataHelper()

		category_messages = []
		tag_messages = []
		venue_messages = []
		organizer_messages = []
		event_messages = []

		# #Fetch All Tags
		all_tags = atl_fetcher_obj.get_all_tags()
		for tag in all_tags:
			tag_message = atl_data_helper_obj.update_or_create_tags(tag)
			if tag_message:
				tag_messages.append(tag_message)

		# #Fetch All Category
		all_category = atl_fetcher_obj.get_all_categories()
		for category in all_category:
			category_message = atl_data_helper_obj.update_or_create_category(category)
			if category_message:
				category_messages.append(category_message)
		
		# #Fetch All Venues
		all_venus = atl_fetcher_obj.get_all_venues()
		for venue in all_venus:
			venue_message = atl_data_helper_obj.update_or_create_venue(venue)
			if venue_message:
				venue_messages.append(venue_message)

		# # #Fetch All Organizers
		all_orgainzer = atl_fetcher_obj.get_all_organizer()
		for organizer in all_orgainzer:
			organizer_message = atl_data_helper_obj.update_or_create_organizer(organizer)
			if organizer_message:
				organizer_messages.append(organizer_message)

		# #Fetch All Events
		all_events = atl_fetcher_obj.get_all_events()
		for event in all_events:
			event_message = atl_data_helper_obj.update_or_create_event(event)
			if event_message:
				event_messages.append(event_message)

		pull_data_result = {"event" : event_messages, "organizer" : organizer_messages, "venue" : venue_messages, "category_messages" : category_messages, "tag_messages" : tag_messages}
		event_pull_log_obj.description = pull_data_result
		event_pull_log_obj.end_time = datetime.datetime.today()
		event_pull_log_obj.status = 1
		event_pull_log_obj.save()
	except Exception as e:
		error_message = str(e)
		event_pull_log_obj.description = {"error_message" : error_message}
		event_pull_log_obj.description = pull_data_result
		event_pull_log_obj.end_time = datetime.datetime.today()
		event_pull_log_obj.status = 2
		event_pull_log_obj.save()