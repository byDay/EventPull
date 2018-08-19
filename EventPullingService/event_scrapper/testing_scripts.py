import requests
from bs4 import BeautifulSoup
# url = 'http://venkmans.com/events/2018-08/'
url = 'http://venkmans.com/event/smokey-jones-and-the-3-dollar-pistols/'
# url = 'https://beltline.org/events/?EventJumpToMonth=09&EventJumpToYear=2018&category='
# url = 'https://www.seatsforeveryone.com/atbs_ajax/events?CityID=34&offset=25'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
req = requests.post(url, headers=hdr)
html_content = req.text
soup = BeautifulSoup(html_content, 'html.parser')
