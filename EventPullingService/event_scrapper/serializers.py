from event_scrapper import models
from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Event
        fields = ('id', 'name','event_id','description','start_date','event_start_time',
                    'end_date','event_end_time','tags','is_all_day_event','venue','category','event_ur','organizer_nam',
                                        'organizer_ur','minimum_cos','event_metadata')