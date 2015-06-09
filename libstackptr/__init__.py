#!/usr/bin/env python
"""
Python client library for stackptr
Copyright 2014-2015 Michael Farrell <http://micolous.id.au>

License: LGPLv3+, see COPYING and COPYING.LESSER
"""

import requests, urlparse, simplejson, datetime, pytz, isodate

STACKPTR_URI = 'https://stackptr.com/'


class TrackedUser(object):
	def __init__(self, raw_data):
		self._raw = raw_data
		
		if 'lastupd' in raw_data and raw_data['lastupd'] not in (None, -1):
			if isinstance(raw_data['lastupd'], int) or isinstance(raw_data['lastupd'], long):
				self._updated = datetime.datetime.fromtimestamp(raw_data['lastupd'], pytz.utc)
			else:
				self._updated = isodate.parse_datetime(raw_data['lastupd'])
		else:
			# "me" data lacks this info.
			self._updated = None
	
	@property
	def updated(self):
		"""
		Last update as datetime
		"""
		return self._updated
	
	@property
	def icon(self):
		return self._raw['icon']

	@property
	def user(self):
		print self._raw
		return self._raw['username']
	
	@property
	def latitude(self):
		return self._raw['loc'][0]
	
	@property
	def longitude(self):
		return self._raw['loc'][1]
	
	def __repr__(self):
		return '<TrackedUser: name=%r, location=%s, %s, updated=%r>' % (
			self.user, self.latitude, self.longitude, self.updated)


class StackPtrClient(object):
	"""
	Client object for stackptr.
	
	:param api_key str: API key used to connect to the stackptr service.
	:param uri str: Root URI of the stackptr service.  Defaults to the master stackptr instance.
	
	"""
	def __init__(self, api_key, uri=None):
		if uri is None:
			uri = STACKPTR_URI
		self._uri = uri
		self._api_key = api_key

	def _req(self, path, params=None, json=False):
		path = urlparse.urljoin(self._uri, path)
		if params is None:
			response = requests.get(path, params={'apikey': self._api_key})
		else:
			params['apikey'] = self._api_key
			response = requests.post(path, data=params)
		
		if json:
			return response.json(use_decimal=True)
		else:
			return response

	def test(self):
		return self._req('/test')

	def update(self, latitude, longitude, altitude=0, heading=-1, speed=-1):
		"""
		Update the user's current location.
		
		"""
		if heading == -1:
			speed = -1
		
		assert -90 <= latitude <= 90, 'Latitude must be in range -90..90'
		assert -180 <= latitude <= 180, 'Longitude must be in range -180..180'
		
		self._req('/update', params=dict(
			lat=latitude,
			lon=longitude,
			alt=altitude,
			hdg=heading,
			spd=speed
		))

	def users(self):
		"""
		Gets a list of users that are followed
		
		Tuple of (my location, followed users)
		"""
		
		r = self._req('/users', json=True)
		me = None
		following = []
		for user in r:
			if user['type'] == 'user-me':
				me = TrackedUser(user['data'])
			elif user['type'] == 'user':
				if (isinstance(user['data'], dict):
					# old proto
					following.append([TrackedUser(x) for x in user['data'].itervalues()])
				else:
					# new proto
					following.append([TrackedUser(x) for x in user['data']])
		return me, following

