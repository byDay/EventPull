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
		endpoint = "events/"
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_events = requests.get(endpoint_url, headers=self.HEADERS)
			if all_events.stats_code == 200:
				return all_events.json()['events']
			else:
				return []
		except:
			return []

	def get_event_by_id(self, event_id):
		endpoint = "events/" + str(event_id)
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_events = requests.get(endpoint_url, headers=self.HEADERS)
			if all_events.stats_code == 200:
				return all_events.json()
			else:
				return {}
		except:
			return {}

	def get_all_venues(self):
		endpoint = "venues/"
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_events = requests.get(endpoint_url, headers=self.HEADERS)
			if all_events.stats_code == 200:
				return all_events.json()['venues']
			else:
				return []
		except:
			return []

	def get_venue_by_id(self, venue_id):
		endpoint = "events/" + str(venue_id)
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_venues = requests.get(endpoint_url, headers=self.HEADERS)
			if all_venues.stats_code == 200:
				return all_venues.json()
			else:
				return {}
		except:
			return {}

	def get_all_organizer(self):
		endpoint = "organizers/"
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_events = requests.get(endpoint_url, headers=self.HEADERS)
			if all_events.stats_code == 200:
				return all_events.json()['organizers']
			else:
				return []
		except:
			return []

	def get_organizer_by_id(self, organizer_id):
		endpoint = "events/" + str(organizer_id)
		endpoint_url = self.BASE_URL + endpoint
		try:
			all_organizer = requests.get(endpoint_url, headers=self.HEADERS)
			if all_organizer.stats_code == 200:
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
			if event.stats_code == 200:
				return event.json()
			else:
				return {}
		except:
			return {}

	def create_organizer(self, organizer):
		endpoint = "events/"
		endpoint_url = self.BASE_URL + endpoint
		try:
			organizer = requests.post(endpoint_url, data=json.dumps(event), headers=self.HEADERS)
			if organizer.stats_code == 200:
				return organizer.json()
			else:
				return {}
		except:
			return {}

	def create_venue(self, venue):
		endpoint = "events/"
		endpoint_url = self.BASE_URL + endpoint
		try:
			venue = requests.post(endpoint_url, data=json.dumps(event), headers=self.HEADERS)
			if venue.stats_code == 200:
				return venue.json()
			else:
				return {}
		except:
			return {}