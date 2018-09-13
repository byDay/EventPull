from import_export import resources
from event_scrapper.models import Event, Venue


class EventResource(resources.ModelResource):
    class Meta:
        model = Event
        fields = ('name', 'event_id', 'description', 'start_date', 'event_start_time',
                  'end_date', 'event_end_time', 'tags', 'is_all_day_event', 'venue', 'category', 'event_url', 'organizer_name',
                  'organizer_url', 'minimum_cost')
        exclude = ('id', 'organizer_url', 'event_metadata')


class VenueResource(resources.ModelResource):
    class Meta:
        model = Venue
        exclude = ('id', 'url_config', 'scraping_config', 'venue_metadata')
