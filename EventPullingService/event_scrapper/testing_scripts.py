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
tasks.process_venue_scrapping(1)
