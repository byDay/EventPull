from __future__ import absolute_import

import time
import celery
import requests
import datetime
from bs4 import BeautifulSoup
from celery import shared_task
from event_scrapper import models
from celery.schedules import crontab
from venue_scrapper import VenueScrapper
from celery.decorators import task, periodic_task

headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
			'Accept-Encoding': 'none', 
			'Accept-Language': 'en-US,en;q=0.8', 
			'Connection': 'keep-alive'
		}

#@celery.decorators.periodic_task(run_every=crontab(minute='1'))
def trigger_scrapping_cron():
	all_venues = models.Venue.objects.filter(is_active=True)
	for venue in all_venues:
		process_venue_scrapping(venue)

def process_venue_scrapping(venue):
	log = models.ScrapingEventLogs.objects.create(venue=venue, status=0, start_time=datetime.datetime.today())
	
	#Start Scraping
	venue_scrapper_obj = VenueScrapper(venue)
	event_obj_list = venue_scrapper_obj.scrape_venue()




	#End Scraping

	log.end_time = datetime.datetime.today()
	log.status = 1
	log.description = {}
	log.save()
