import requests
import datetime
from bs4 import BeautifulSoup

class VenueScrapper(object):

	def __init__(self, venue):
		self.venue = venue
		self.url_config = venue.url_config
		self.scraping_config = venue.scraping_config
		self.venue_metadata = venue.venue_metadata

	@property
	def venue_url(self):
		return self.url_config['venue_url']

	@property
	def is_venue_website_paginated(self):
		return None

	@property
	def is_venue_scraping_html_based(self):
		return self.is_venue_scraping_html_based

	@property
	def is_venue_scraping_api_based(self):
		return self.is_venue_scraping_api_based

	#This may return mutiple URL's if Venue Website is Paginated based
	#If Paginated Website then Scrape all Url
	#Retrur : [<list of url's>]
	def get_current_month_scrapping_url(self):
		return None

	def get_venue_soup_object(self):
		return None

	def get_main_content_parent_tag(self):
		return None

	def get_event_content_tags(self):
		return []

	"""
	#Steps:
		1. Get all Eligible Urls of Venue Website
		2. For each Venue Website Url. Do the following steps
		3. Fetch Main Content Tag (In most cases : Table Tag)
		4. Fetch Event Tag this Table Tag.
		5. Create Event Object by extracting data from Event Tags and Event Main Url.
		6. Return the Event Object List.
	"""
	def scrape_venue(self):
		return []


class EventScrapper(object):

	def __init__(self, event_dom_tags):
		pass

	def get_all_event_object(self):
		event_obj_list = []
		return event_obj_list
