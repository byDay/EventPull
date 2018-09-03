from event_scrapper import models
from event_scrapper import serializers

class DataHelper(object):

	@staticmethod
	def update_or_create_event(event):
		event['event_id'] = event['id']

		try:
			venue = models.AtlByDayVenue.objects.get(venue_id=event['venue']['id'])
			event.pop('venue')
			event['venue'] = venue.id
		except:
			event.pop('venue')
			event['venue'] = None
		
		try:
			if event['organizer'] and len(event['organizer']) > 0:
				organizer = models.AtlByDayOrganizer.objects.get(organizer_id=event['organizer'][0]['id'])
				event.pop('organizer')
				event['organizer'] = organizer.id
		except:
			event.pop('organizer')
			event['organizer'] = None

		#Check if Event Already Exist
		try:
			event = models.AtlByDayEvent.objects.get(event_id=event['event_id'])
			return 'Event already exist {event_id}'.format(event_id=event['event_id'])
		except:
			pass

		#Create Event
		event_serializers = serializers.AtlByDayEventSerializer(data=event)
		if event_serializers.is_valid():
			event_serializers.save()
			return None
		else:
			return event_serializers.errors


	@staticmethod
	def update_or_create_venue(venue):
		venue['venue_id'] = venue['id']
		
		#Check if Venue Already Exist
		try:
			venue = models.AtlByDayVenue.objects.get(venue_id=venue['venue_id'])
			return 'Venue already exist {venue_id}'.format(venue_id=venue['venue_id'])
		except:
			pass

		#Create Venue
		venue_serializers = serializers.AtlByDayVenueSerializer(data=venue)
		if venue_serializers.is_valid():
			venue_serializers.save()
			return None
		else:
			return venue_serializers.errors
	

	@staticmethod
	def update_or_create_organizer(organizer):
		organizer['organizer_id'] = organizer['id']
		
		#Check if Organizer Already Exist
		try:
			oragnizer = models.AtlByDayOrganizer.objects.get(organizer_id=organizer['organizer_id'])
			return 'Organizer already exist {organizer_id}'.format(organizer_id=organizer['organizer_id'])
		except:
			pass

		#Create Organizer
		oragnizer_serializers = serializers.AtlByDayOrganizerSerializer(data=organizer)
		if oragnizer_serializers.is_valid():
			oragnizer_serializers.save()
			return None
		else:
			return oragnizer_serializers.errors


	@staticmethod
	def update_or_create_tags(tags):
		tags['tag_id'] = tags['id']
		
		#Check if Tag Already Exist
		try:
			tags = models.AtlByDayTag.objects.get(tag_id=tags['tag_id'])
			return 'Tag already exist {tag_id}'.format(tag_id=tags['tag_id'])
		except:
			pass

		#Create Category
		tags_serializers = serializers.AtlByDayTagSerializer(data=tags)
		if tags_serializers.is_valid():
			tags_serializers.save()
			return None
		else:
			return tags_serializers.errors

	@staticmethod
	def update_or_create_category(category):
		category['category_id'] = category['id']
		
		#Check if Category Already Exist
		try:
			category = models.AtlByDayCategory.objects.get(category_id=category['category_id'])
			return 'Category already exist {category_id}'.format(category_id=category['category_id'])
		except:
			pass

		#Create Category
		category_serializers = serializers.AtlByDayCategorySerializer(data=category)
		if category_serializers.is_valid():
			category_serializers.save()
			return None
		else:
			return category_serializers.errors