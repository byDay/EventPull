import json
import requests
from event_scrapper import models
from event_scrapper import serializers

class WPDataHelper(object):

	"""
		WP Data Creation Steps:
			1. Check in Local DB if Data Exist.
			2. Else create in WP and Sync
	
	Sample Event Create Obj Keys:
	
	['website', 'status', 'description', 'end_date', 'tags', 'global_id_lineage', 
	'image', 'excerpt', 'sticky', 'cost_details', 'featured', 'cost', 'show_map_link', 
	'global_id', 'modified', 'date', 'timezone', 'end_date_details', 'utc_start_date_details', 
	'id', 'categories', 'slug', 'author', 'event_id', 'show_map', 'title', 'all_day', 
	'start_date_details', 'utc_end_date', 'timezone_abbr', 'url', 'date_utc', 
	'utc_end_date_details', 'rest_url', 'utc_start_date', 'start_date', 'modified_utc', 'hide_from_listings']

	"""

	BASE_URL = "https://atlbyday.com/wp-json/tribe/events/v1/"
	TOKEN = "Basic RXZlbnRQdWxsOldRZlJycHRkTHlsa0U1dzI="
	HEADERS = {
		"Authorization" : TOKEN,
		"Content-Type" : "application/json"
	}

	EVENT_KEY_MAPPING = {
						    'website' : 'event_url',
						    'status' : None,
						    'description' : 'description',
						    'end_date' : 'event_end_time',
						    'tags' : 'tags:tags',
						    'cost' : 'minimum_cost',
						    'categories' : 'category',
						    'title' : 'name',
						    'all_day' : 'is_all_day_event',
						    'start_date' : 'event_start_time',
						    'venue' : 'venue',
						    'orgainzer' : 'orgainzer'
						}

	VENUE_KEY_MAPPING = {
							'venue' : 'name',
							'website' : 'venue_metadata:url'
						}

	@staticmethod
	def create_wp_event(event):
		pass

	@staticmethod
	def create_wp_category(category):
		endpoint = 'categories/'
		endpoint = WPDataHelper.BASE_URL + endpoint
		category_request = requests.post(endpoint, headers=WPDataHelper.HEADERS, data=json.dumps(category))
		if category_request.status_code == 201:
			return category_request.json()
		else:
			print 'Error occured while creating WP category : {category}'.format(category=category)
			return None

	@staticmethod
	def create_wp_tag(tag):
		endpoint = 'tags/'
		endpoint = WPDataHelper.BASE_URL + endpoint
		tag_request = requests.post(endpoint, headers=WPDataHelper.HEADERS, data=json.dumps(tag))
		if tag_request.status_code == 201:
			return tag_request.json()
		else:
			print 'Error occured while creating WP tags : {tag}'.format(tag=tag)
			return None

	@staticmethod
	def create_wp_orgainzer(organizer):
		endpoint = 'organizers/'
		endpoint = WPDataHelper.BASE_URL + endpoint
		organizer_request = requests.post(endpoint, headers=WPDataHelper.HEADERS, data=json.dumps(organizer))
		if organizer_request.status_code == 201:
			return organizer_request.json()
		else:
			print 'Error occured while creating WP organizer : {organizer}'.format(organizer=organizer)
			return None

	@staticmethod
	def create_wp_venue(venue):
		endpoint = 'venues/'
		endpoint = WPDataHelper.BASE_URL + endpoint
		venue_request = requests.post(endpoint, headers=WPDataHelper.HEADERS, data=json.dumps(venue))
		if venue_request.status_code == 201:
			return venue_request.json()
		else:
			print 'Error occured while creating WP Venue : {venue}'.format(venue=venue)
			return None


class DataHelper(object):

	@staticmethod
	def update_or_create_event(event):
		event['event_id'] = event['id']
		event['organizer'] = None
		event['venue'] = None
		
		try:
			venue = models.AtlByDayVenue.objects.get(venue_id=event['venue']['id'])
			event['venue'] = venue.id
		except:
			event['venue'] = None
		
		try:
			if event['organizer'] and len(event['organizer']) > 0:
				organizer = models.AtlByDayOrganizer.objects.get(organizer_id=event['organizer'][0]['id'])
				event['organizer'] = organizer.id
		except:
			event['organizer'] = None
		
		event.pop('venue')
		event.pop('organizer')

		#Check if Event Already Exist
		try:
			event_obj = models.AtlByDayEvent.objects.get(event_id=event['event_id'])
			return 'Event already exist {event_id}'.format(event_id=event['event_id'])
		except:
			pass

		#Create Event
		event_serializers = serializers.AtlByDayEventSerializer(data=event)
		if event_serializers.is_valid():
			event_serializers.save()
			return None
		else:
			return 'EventID : {event_id}'.format(event_id=event['id']) + str(event_serializers.errors)


	@staticmethod
	def update_or_create_venue(venue):
		venue['venue_id'] = venue['id']
		
		#Check if Venue Already Exist
		try:
			venue_obj = models.AtlByDayVenue.objects.get(venue_id=venue['venue_id'])
			return 'Venue already exist {venue_id}'.format(venue_id=venue['venue_id'])
		except:
			pass

		#Create Venue
		venue_serializers = serializers.AtlByDayVenueSerializer(data=venue)
		if venue_serializers.is_valid():
			venue_serializers.save()
			return None
		else:
			return 'VenueID : {venue_id}'.format(venue_id=venue['id']) + str(venue_serializers.errors)
	

	@staticmethod
	def update_or_create_organizer(organizer):
		organizer['organizer_id'] = organizer['id']
		
		#Check if Organizer Already Exist
		try:
			oragnizer_obj = models.AtlByDayOrganizer.objects.get(organizer_id=organizer['organizer_id'])
			return 'Organizer already exist {organizer_id}'.format(organizer_id=organizer['organizer_id'])
		except:
			pass

		#Create Organizer
		oragnizer_serializers = serializers.AtlByDayOrganizerSerializer(data=organizer)
		if oragnizer_serializers.is_valid():
			oragnizer_serializers.save()
			return None
		else:
			return 'Organizer : {organizer_id}'.format(organizer_id=organizer['id']) + str(oragnizer_serializers.errors)


	@staticmethod
	def update_or_create_tags(tags):
		tags['tag_id'] = tags['id']
		
		#Check if Tag Already Exist
		try:
			tags_obj = models.AtlByDayTag.objects.get(tag_id=tags['tag_id'])
			return 'Tag already exist {tag_id}'.format(tag_id=tags['tag_id'])
		except:
			pass

		#Create Category
		tags_serializers = serializers.AtlByDayTagSerializer(data=tags)
		if tags_serializers.is_valid():
			tags_serializers.save()
			return None
		else:
			return 'Tags : {tag_id}'.format(tag_id=tags['id']) + str(tags_serializers.errors)

	@staticmethod
	def update_or_create_category(category):
		category['category_id'] = category['id']
		
		#Check if Category Already Exist
		try:
			category_obj = models.AtlByDayCategory.objects.get(category_id=category['category_id'])
			return 'Category already exist {category_id}'.format(category_id=category['category_id'])
		except:
			pass

		#Create Category
		category_serializers = serializers.AtlByDayCategorySerializer(data=category)
		if category_serializers.is_valid():
			category_serializers.save()
			return None
		else:
			return 'Category : {category_id}'.format(category_id=category['id']) + str(category_serializers.errors)