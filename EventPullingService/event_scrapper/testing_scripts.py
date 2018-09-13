import dryscrape
import requests
from bs4 import BeautifulSoup
dryscrape.start_xvfb()
session = dryscrape.Session()
url = 'https://www.seatsforeveryone.com/3566807/WizKhalifaandRaeSremmurd'
session.visit(url)
response = session.body()
soup = BeautifulSoup(response)

from event_scrapper import serializers
evs = serializers.EventSerializer(data=x)
evs.is_valid()


from event_scrapper import tasks
tasks.trigger_scrapping_cron()
from event_scrapper import tasks
tasks.pull_data_from_atlbyday_wordpress()
from event_scrapper import tasks
tasks.process_venue_scrapping(1)


from event_scrapper import models
event_ids = models.AtlByDayEvent.objects.filter(venue_id__in=[600, 601, 602, 603, 604]).values_list('event_id', flat=True)
url = 'https://atlbyday.com/wp-json/tribe/events/v1/events/{id}'
TOKEN = "Basic RXZlbnRQdWxsOldRZlJycHRkTHlsa0U1dzI="
HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}
for i in event_ids:
    xx = url
    xx = xx.format(id=i)
    r = requests.delete(xx, headers=HEADERS)
    print r.status_code
