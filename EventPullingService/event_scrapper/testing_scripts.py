import requests
from bs4 import BeautifulSoup
url = 'http://www.ticketfly.com/event/1710114?utm_medium=api'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
req = requests.post(url, headers=hdr)
html_content = req.text
soup = BeautifulSoup(html_content, 'html.parser')

from event_scrapper import serializers
evs = serializers.EventSerializer(data=x)
evs.is_valid()


from event_scrapper import tasks
tasks.trigger_scrapping_cron()
