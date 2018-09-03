from event_scrapper import models
from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Event
        fields = ('id', 'name','event_id','description','start_date','event_start_time',
                    'end_date','event_end_time','tags','is_all_day_event','venue','category','event_url','organizer_name',
                                        'organizer_url','minimum_cost','event_metadata')


class AtlByDayVenueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AtlByDayVenue
        fields = "__all__"

class AtlByDayOrganizerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AtlByDayOrganizer
        fields = "__all__"

class AtlByDayEventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AtlByDayEvent
        fields = "__all__"