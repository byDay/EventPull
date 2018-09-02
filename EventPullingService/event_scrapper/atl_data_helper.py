from event_scrapper import models
from event_scrapper import serializers

class DataHelper(object):

	@staticmethod
	def update_or_create_event(event):
		pass


	@staticmethod
	def update_or_create_venue(venue):
		pass
	

	@staticmethod
	def update_or_create_organizer(organizer):
		organizer.pop("date")
		organizer.pop("date_utc")
		organizer.pop("modified")
		organizer.pop("modified_utc")
		organizer['organizer_id'] = organizer['id']
		organizer.pop("id")
		
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
