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
				endpoint = "events/" + "?page={page_no}"
				endpoint_url = self.BASE_URL + endpoint
				endpoint_url = endpoint_url.format(page_no=page_no)
				print endpoint_url
				page_no = page_no + 1
				all_events = requests.get(endpoint_url, headers=self.HEADERS)
				if all_events.status_code == 200:
					all_events_list = all_events_list + all_events.json()['events']
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
				endpoint = "venues/" + "?page={page_no}"
				endpoint_url = self.BASE_URL + endpoint
				endpoint_url = endpoint_url.format(page_no=page_no)
				print endpoint_url
				page_no = page_no + 1
				all_venues = requests.get(endpoint_url, headers=self.HEADERS)
				if all_venues.status_code == 200:
					all_venues_list = all_venues_list + all_venues.json()['venues']
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
				endpoint = "organizers/" + "?page={page_no}"
				endpoint_url = self.BASE_URL + endpoint
				endpoint_url = endpoint_url.format(page_no=page_no)
				print endpoint_url
				page_no = page_no + 1
				all_organizers = requests.get(endpoint_url, headers=self.HEADERS)
				if all_organizers.status_code == 200:
					all_organizers_list = all_organizers_list + all_organizers.json()['organizers']
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