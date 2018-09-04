import json
import requests

class AtlDataFetcher(object):

	BASE_URL = "https://atlbyday.com/wp-json/tribe/events/v1/"
	TOKEN = "Basic RXZlbnRQdWxsOldRZlJycHRkTHlsa0U1dzI="
	HEADERS = {
		"Authorization" : TOKEN,
		"Content-Type" : "application/json"
	}

	def __init__(self):
		pass

	def get_all_events(self):
		page_no = 1
		all_events_list = []
		try:
			while 1:
				endpoint = "events/" + "?page={page_no}&per_page=50&start_date=1960-09-04"
				endpoint_url = self.BASE_URL + endpoint
				endpoint_url = endpoint_url.format(page_no=page_no)
				print endpoint_url
				page_no = page_no + 1
				all_events = requests.get(endpoint_url, headers=self.HEADERS)

				if all_events.status_code == 200:
					if len(all_events.json()['events']) > 0:
						all_events_list = all_events_list + all_events.json()['events']
					else:
						return all_events_list
				if all_events.status_code == 404:
					break
		except:
			return all_events_list
		return all_events_list

	def get_event_by_id(self, event_id):
		endpoint = "events/" + str(event_id)
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_events = requests.get(endpoint_url, headers=self.HEADERS)
			if all_events.status_code == 200:
				return all_events.json()
			else:
				return {}
		except:
			return {}

	def get_all_venues(self):
		page_no = 1
		all_venues_list = []
		try:
			while 1:
				endpoint = "venues/" + "?page={page_no}&per_page=50"
				endpoint_url = self.BASE_URL + endpoint
				endpoint_url = endpoint_url.format(page_no=page_no)
				print endpoint_url
				page_no = page_no + 1
				all_venues = requests.get(endpoint_url, headers=self.HEADERS)
				if all_venues.status_code == 200:
					if len(all_venues.json()['venues']) > 0:
						all_venues_list = all_venues_list + all_venues.json()['venues']
					else:
						return all_venues_list
				if all_venues.status_code == 404:
					break
		except:
			return all_venues_list
		return all_venues_list

	def get_venue_by_id(self, venue_id):
		endpoint = "venues/" + str(venue_id)
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_venues = requests.get(endpoint_url, headers=self.HEADERS)
			if all_venues.status_code == 200:
				return all_venues.json()
			else:
				return {}
		except:
			return {}

	def get_all_organizer(self):
		page_no = 1
		all_organizers_list = []
		try:
			while 1:
				endpoint = "organizers/" + "?page={page_no}&per_page=50"
				endpoint_url = self.BASE_URL + endpoint
				endpoint_url = endpoint_url.format(page_no=page_no)
				print endpoint_url
				page_no = page_no + 1
				all_organizers = requests.get(endpoint_url, headers=self.HEADERS)
				if all_organizers.status_code == 200:
					if len(all_organizers.json()['organizers']) > 0:
						all_organizers_list = all_organizers_list + all_organizers.json()['organizers']
					else:
						return all_organizers_list
				if all_organizers.status_code == 404:
					break
		except:
			return all_organizers_list
		return all_organizers_list

	def get_organizer_by_id(self, organizer_id):
		endpoint = "organizers/" + str(organizer_id)
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_organizer = requests.get(endpoint_url, headers=self.HEADERS)
			if all_organizer.status_code == 200:
				return all_organizer.json()
			else:
				return {}
		except:
			return {}

	def create_event(self, event):
		endpoint = "events/"
		endpoint_url = self.BASE_URL + endpoint
		try:
			event = requests.post(endpoint_url, data=json.dumps(event), headers=self.HEADERS)
			if event.status_code == 200:
				return event.json()
			else:
				return {}
		except:
			return {}

	def create_organizer(self, organizer):
		endpoint = "organizers/"
		endpoint_url = self.BASE_URL + endpoint
		try:
			organizer = requests.post(endpoint_url, data=json.dumps(event), headers=self.HEADERS)
			if organizer.status_code == 200:
				return organizer.json()
			else:
				return {}
		except:
			return {}

	def create_venue(self, venue):
		endpoint = "venues/"
		endpoint_url = self.BASE_URL + endpoint
		try:
			venue = requests.post(endpoint_url, data=json.dumps(event), headers=self.HEADERS)
			if venue.status_code == 200:
				return venue.json()
			else:
				return {}
		except:
			return {}

	def get_all_tags(self):
		page_no = 1
		all_tags_list = []
		try:
			while 1:
				endpoint = "tags/" + "?page={page_no}&per_page=50"
				endpoint_url = self.BASE_URL + endpoint
				endpoint_url = endpoint_url.format(page_no=page_no)
				print endpoint_url
				page_no = page_no + 1
				all_tags = requests.get(endpoint_url, headers=self.HEADERS)
				if all_tags.status_code == 200:
					if len(all_tags.json()['tags']) > 0:
						all_tags_list = all_tags_list + all_tags.json()['tags']
					else:
						return all_tags_list
				if all_tags.status_code == 404:
					break
		except:
			return all_tags_list
		return all_tags_list

	def get_tags_by_id(self, tag_id):
		endpoint = "tags/" + str(tag_id)
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_tags = requests.get(endpoint_url, headers=self.HEADERS)
			if all_tags.status_code == 200:
				return all_tags.json()
			else:
				return {}
		except:
			return {}

	def get_all_categories(self):
		page_no = 1
		all_categories_list = []
		try:
			while 1:
				endpoint = "categories/" + "?page={page_no}&per_page=50"
				endpoint_url = self.BASE_URL + endpoint
				endpoint_url = endpoint_url.format(page_no=page_no)
				print endpoint_url
				page_no = page_no + 1
				all_categories = requests.get(endpoint_url, headers=self.HEADERS)
				if all_categories.status_code == 200:
					if len(all_categories.json()['categories']) > 0:
						all_categories_list = all_categories_list + all_categories.json()['categories']
					else:
						return all_categories_list
				if all_categories.status_code == 404:
					break
		except:
			return all_categories_list
		return all_categories_list

	def get_tags_by_id(self, category_id):
		endpoint = "categories/" + str(category_id)
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_categories = requests.get(endpoint_url, headers=self.HEADERS)
			if all_categories.status_code == 200:
				return all_categories.json()
			else:
				return {}
		except:
			return {}