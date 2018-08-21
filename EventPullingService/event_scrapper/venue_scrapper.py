import re
import sys
import requests
import calendar
import datetime
import dryscrape
from bs4 import BeautifulSoup

if 'linux' in sys.platform:
    dryscrape.start_xvfb()

class VenueScrapper(object):

	HEADERS = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
			'Accept-Encoding': 'none', 
			'Accept-Language': 'en-US,en;q=0.8', 
			'Connection': 'keep-alive'
		}

	def __init__(self, venue):
		self.venue = venue
		self.url_config = venue.url_config
		self.scraping_config = venue.scraping_config
		self.venue_metadata = venue.venue_metadata

	@property
	def venue_url(self):
		return self.url_config['venue_url']

	@property
	def is_venue_website_paginated(self):
		if self.url_config and 'is_paginated' in self.url_config:
			return self.url_config['is_paginated']
		else:
			return False

	@property
	def is_venue_scraping_html_based(self):
		if self.url_config and 'return_type' in self.url_config and self.url_config['return_type'] == 'HTML':
			return True
		else:
			return False

	@property
	def is_venue_scraping_api_based(self):
		if self.url_config and 'return_type' in self.url_config and self.url_config['return_type'] == 'API':
			return True
		else:
			return False

	def add_one_month(self, t):
	    """Return a `datetime.date` or `datetime.datetime` (as given) that is
	    one month earlier.
	    
	    Note that the resultant day of the month might change if the following
	    month has fewer days:
	    
	        >>> add_one_month(datetime.date(2010, 1, 31))
	        datetime.date(2010, 2, 28)
	    """
	    import datetime
	    one_day = datetime.timedelta(days=1)
	    one_month_later = t + one_day
	    while one_month_later.month == t.month:  # advance to start of next month
	        one_month_later += one_day
	    target_month = one_month_later.month
	    while one_month_later.day < t.day:  # advance to appropriate day
	        one_month_later += one_day
	        if one_month_later.month != target_month:  # gone too far
	            one_month_later -= one_day
	            break
	    return one_month_later

	def subtract_one_month(self, t):
	    """Return a `datetime.date` or `datetime.datetime` (as given) that is
	    one month later.
	    
	    Note that the resultant day of the month might change if the following
	    month has fewer days:
	    
	        >>> subtract_one_month(datetime.date(2010, 3, 31))
	        datetime.date(2010, 2, 28)
	    """
	    import datetime
	    one_day = datetime.timedelta(days=1)
	    one_month_earlier = t - one_day
	    while one_month_earlier.month == t.month or one_month_earlier.day > t.day:
	        one_month_earlier -= one_day
	    return one_month_earlier

	#This may return mutiple URL's if Venue Website is Paginated based
	#If Paginated Website then Scrape all Url
	#Retrur : [<list of url's>]
	def get_current_month_scrapping_url(self):
		urls = []
		today_date = datetime.datetime.today().date()
		today_date = self.add_one_month(today_date)
		month_start_date = today_date.replace(day=1)
		month_end_date = today_date.replace(day=calendar.monthrange(today_date.year, today_date.month)[1])
		venue_url = self.url_config['venue_url']
		ext_params, url_params = None, None
		if self.url_config and 'ext_params' in self.url_config:
			ext_params = self.url_config['ext_params']
		if self.url_config and 'url_params' in self.url_config:
			url_params = self.url_config['url_params']

		range_values = []
		if url_params and len(url_params.keys()) > 0:
			param_value_dict = {}
			for key, value in url_params.iteritems():
				if 'type' in value:
					param_value = ''
					if value['type'] == 'int':
						param_value = value['value']
					if value['type'] == 'date' and 'format' in value:
						formated_value = today_date.strftime(value['format'])
						param_value = str(formated_value)
					if value['type'] == 'range':
						param_value = '{range_value}'
						for i in range(value['start_value'], value['end_value'] + 1):
							range_values.append(i*value['increment_by'])
					param_value_dict[key] = param_value
			venue_url = venue_url.format(**param_value_dict)

		if ext_params and len(ext_params.keys()) > 0:
			for key, value in ext_params.iteritems():
				if 'type' in value:
					param_value = ''
					if value['type'] == 'bool':
						param_value = str(key) + '=' + str(value['value'])
					if value['type'] == 'string':
						param_value = str(key) + '=' + str(value['value'])
					if value['type'] == 'int':
						param_value = str(key) + '=' + str(value['value'])
					if value['type'] == 'date' and 'format' in value:
						selected_date = today_date
						if 'range' in value and value['range'] == 'max':
							selected_date = month_end_date
						if 'range' in value and value['range'] == 'min':
							selected_date = month_start_date
						formated_value = selected_date.strftime(value['format'])
						param_value = key + '=' + str(formated_value)
					if value['type'] == 'range':
						param_value = str(key) + '=' + '{range_value}'
						for i in range(value['start_value'], value['end_value'] + 1):
							range_values.append(i*value['increment_by'])
					venue_url = venue_url + param_value + '&'

		if len(range_values) > 0:
			for r_idx in range_values:
				temp_url = venue_url
				temp_url = temp_url.format(range_value=r_idx)
				urls.append(temp_url)
		else:
			urls.append(venue_url)

		return urls

	def get_venue_soup_object(self, scrap_url):
		req = requests.post(scrap_url, headers=self.HEADERS)
		response = req.text
		self.venue_soup_obj = BeautifulSoup(response, 'html.parser')
		return self.venue_soup_obj

	def get_event_objects_from_api(self, scrap_url):
		api_data_config = self.url_config
		url_response = requests.get(scrap_url, headers=self.HEADERS)
		response_dict = url_response.json()
		if 'key' in api_data_config:
			key = api_data_config['key']
			all_keys_hieracrhy = key.split(':')
			for k in all_keys_hieracrhy:
				response_dict = response_dict[k]
		return response_dict

	def get_main_content_parent_tag(self, scrap_url):
		venue_soup_obj = self.get_venue_soup_object(scrap_url)
		main_content_tag_config = self.scraping_config['main_content_tag']
		filter_attributes = {}
		for attr in main_content_tag_config['attribute']:
			for key, value in attr.iteritems():
				filter_attributes[key] = value
		main_content_tag = venue_soup_obj.find_all(main_content_tag_config['tag'], attrs=filter_attributes)
		if main_content_tag and len(main_content_tag) > 0:
			return main_content_tag[main_content_tag_config['index']]
		return None

	def get_event_content_tags(self, main_content_tag):
		event_content_tag_config = self.scraping_config['event_content_tag']
		event_metadata_tag_config = event_content_tag_config['event_metadata']
		filter_attributes = {}
		for attr in event_metadata_tag_config['attribute']:
			if 'is_regex' in attr:
				for key, value in attr.iteritems():
					if key != 'is_regex':
						filter_attributes[key] = re.compile(value)
			else:
				for key, value in attr.iteritems():
					filter_attributes[key] = value
		event_content_tags = main_content_tag.find_all(event_metadata_tag_config['tag'], attrs=filter_attributes)
		if event_content_tags and len(event_content_tags):
			return event_content_tags
		return None

	"""
	#Steps:
		1. Get all Eligible Urls of Venue Website
		2. For each Venue Website Url. Do the following steps
		3. Fetch Main Content Tag (In most cases : Table Tag)
		4. Fetch Event Tag this Table Tag.
		5. Create Event Object by extracting data from Event Tags and Event Main Url.
		6. Return the Event Object List.
	"""
	def scrape_venue(self):
		scraping_urls = self.get_current_month_scrapping_url()
		event_obj_list = []
		for scrap_url in scraping_urls:
			if self.is_venue_scraping_api_based:
				event_objects_json = self.get_event_objects_from_api(scrap_url)
				event_objs = EventScrapper(self.venue, 'API', event_objects_json).get_all_event_object()
				event_obj_list = event_obj_list + event_objs
			if self.is_venue_scraping_html_based:
				main_content_tag = self.get_main_content_parent_tag(scrap_url)
				event_content_tags = self.get_event_content_tags(main_content_tag)
				event_objs = EventScrapper(self.venue, 'HTML', event_content_tags).get_all_event_object()
				event_obj_list = event_obj_list + event_objs
		return event_obj_list


class EventScrapper(object):

	HEADERS = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
			'Accept-Encoding': 'none', 
			'Accept-Language': 'en-US,en;q=0.8', 
			'Connection': 'keep-alive'
		}

	event_attributes = ['name','event_id','description','start_date','event_start_time','end_date','event_end_time','tags','is_all_day_event','venue','category','event_url','organizer_name','organizer_url','minimum_cost']

	def __init__(self, venue, event_scrap_type, event_contents):
		self.venue = venue
		self.session = None
		self.event_scrap_type = event_scrap_type
		self.event_soup_object_map = {}
		self.scraping_config = venue.scraping_config
		self.event_contents = event_contents

	def get_ascii_string(self, string):
		if string:
			return ''.join([i if ord(i) < 128 else ' ' for i in string])
		return None

	def get_dryscape_session(self):
		if self.session:
			self.session.reset()
			return self.session
		else:
			self.session = dryscrape.Session()
			return self.session

	def get_event_soup_object(self, event_scrap_url):
		try:
			if event_scrap_url in self.event_soup_object_map:
				return self.event_soup_object_map[event_scrap_url]
			else:
				req = requests.post(event_scrap_url, headers=self.HEADERS, timeout=5)
				response = req.text
				if response and len(response) > 0:
					response = req.text
				else:
					session = self.get_dryscape_session()
					session.visit(event_scrap_url)
					response = session.body()
				event_soup_object = BeautifulSoup(response, 'html.parser')
				return event_soup_object
		except:
			pass

	def get_event_scrap_url_from_tag_object(self, event_tag):
		event_content_tag_config = self.scraping_config['event_content_tag']
		event_url_config = event_content_tag_config['event_url']
		filter_attributes = {}
		for attr in event_url_config['attribute']:
			if 'is_regex' in attr:
				for key, value in attr.iteritems():
					if key != 'is_regex':
						filter_attributes[key] = re.compile(value)
			else:
				for key, value in attr.iteritems():
					filter_attributes[key] = value
		event_url_tags = event_tag.find(event_url_config['tag'], attrs=filter_attributes)
		event_scrap_url = event_url_tags[event_url_config['attribute_key']]
		if 'parent_url' in event_url_config:
			event_scrap_url = event_url_config['parent_url'] + event_scrap_url
		return event_scrap_url

	def get_event_scrap_url_from_json_object(self, json_object):
		event_content_tag_config = self.scraping_config['event_content_tag']
		event_url_config = event_content_tag_config['event_url']
		return json_object[event_url_config['tag']]

	def get_event_attribute_scrap_config(self, attribute_name):
		event_content_tag_config = self.scraping_config['event_content_tag']
		return event_content_tag_config.get(attribute_name, {})

	def get_formatted_date(self, date_string, in_format, out_format):
		try:
			if type(in_format) == list:
				for i_format in in_format:
					try:
						date_object = datetime.datetime.strptime(date_string, i_format)
						#Set Current Year
						date_object = date_object.replace(year=datetime.datetime.today().date().year)
						formated_value = date_object.strftime(out_format)
						return formated_value
					except:
						pass
			else:
				date_object = datetime.datetime.strptime(date_string, in_format)
				#Set Current Year
				date_object = date_object.replace(year=datetime.datetime.today().date().year)
				formated_value = date_object.strftime(out_format)
				return formated_value
		except:
			return None
		return None

	def get_value_from_json_object(self, key_name, json_object):
		key_list = key_name.split(':')
		for key in key_list:
			json_object = json_object[key]
		return json_object

	def get_event_attribute_data(self, attribute_name, event_soup_object, event_json_object=None):
		attribute_scraping_config = self.get_event_attribute_scrap_config(attribute_name)
		if attribute_scraping_config and len(attribute_scraping_config.keys()) > 0:
			filter_attributes = {}

			#Inherit Attribute
			if 'inherit_from' in attribute_scraping_config:
				inherited_data_value = self.get_event_attribute_data(attribute_scraping_config['inherit_from'], event_soup_object, event_json_object=event_json_object)
				if 'type' in attribute_scraping_config and attribute_scraping_config['type'] == 'date':
					inherited_data_value = self.get_formatted_date(inherited_data_value, attribute_scraping_config['in_format'], attribute_scraping_config['out_format'])
					return inherited_data_value

			#Json Based Object
			if event_json_object and 'is_json_based' in attribute_scraping_config:
				value_from_json_object = self.get_value_from_json_object(attribute_scraping_config['key'], event_json_object)
				if 'type' in attribute_scraping_config and attribute_scraping_config['type'] == 'date':
					value_from_json_object = self.get_formatted_date(value_from_json_object, attribute_scraping_config['in_format'], attribute_scraping_config['out_format'])
				return value_from_json_object

			#Attribute Filter
			for attr in attribute_scraping_config['attribute']:
				if 'is_regex' in attr:
					for key, value in attr.iteritems():
						if key != 'is_regex':
							filter_attributes[key] = re.compile(value)
				else:
					for key, value in attr.iteritems():
						filter_attributes[key] = value

			#String based Filter
			string_filter = None
			if 'string' in attribute_scraping_config:
				string_filter = re.compile(attribute_scraping_config['string']['regex_str'])
			
			event_attr_tag = event_soup_object.find(attribute_scraping_config['tag'], string=string_filter, attrs=filter_attributes)
			event_attr_value = None

			if event_attr_tag:
				#Look for Sibling
				if 'sibilings' in attribute_scraping_config:
					event_attr_tag = event_attr_tag.find_next_siblings(attribute_scraping_config['sibilings']['tag'])
					if event_attr_tag and len(event_attr_tag) > 0:
						event_attr_tag = event_attr_tag[attribute_scraping_config['sibilings']['index']]
				if 'tag_property' in attribute_scraping_config and attribute_scraping_config['tag_property']:
					event_attr_value = getattr(event_attr_tag, attribute_scraping_config['tag_property'])
					if 'type' in attribute_scraping_config and attribute_scraping_config['type'] == 'date':
						event_attr_value = self.get_formatted_date(event_attr_value, attribute_scraping_config['in_format'], attribute_scraping_config['out_format'])
				if 'tag_key' in attribute_scraping_config and attribute_scraping_config['tag_key']:
					event_attr_value = event_attr_tag[attribute_scraping_config['tag_key']]
					if 'type' in attribute_scraping_config and attribute_scraping_config['type'] == 'date':
						event_attr_value = self.get_formatted_date(event_attr_value, attribute_scraping_config['in_format'], attribute_scraping_config['out_format'])
			event_attr_value = self.get_ascii_string(event_attr_value)
			return event_attr_value
		return None

	def get_all_event_object(self):
		event_obj_list = []
		if self.event_scrap_type == 'API':
			for event in self.event_contents:
				event_object = {}
				scrap_url = self.get_event_scrap_url_from_json_object(event)
				current_event_soup_object = self.get_event_soup_object(scrap_url)
				for attribute in self.event_attributes:
					event_object[attribute] = self.get_event_attribute_data(attribute, current_event_soup_object, event_json_object=event)
				event_object['venue'] = self.venue.id
				event_object['event_url'] = scrap_url
				event_obj_list.append(event_object)
		if self.event_scrap_type == 'HTML':
			for event in self.event_contents:
				event_object = {}
				scrap_url = self.get_event_scrap_url_from_tag_object(event)
				current_event_soup_object = self.get_event_soup_object(scrap_url)
				for attribute in self.event_attributes:
					event_object[attribute] = self.get_event_attribute_data(attribute, current_event_soup_object)
				event_object['venue'] = self.venue.id
				event_object['event_url'] = scrap_url
				event_obj_list.append(event_object)
		
		return event_obj_list
