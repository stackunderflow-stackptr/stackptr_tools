#!/usr/bin/env python
"""
Python client library for stackptr
Copyright 2014 Michael Farrell <http://micolous.id.au>

License: 3-clause BSD, see COPYING
"""

import requests, urlparse, simplejson, datetime, pytz

STACKPTR_URI = 'https://stackptr.com/'


class TrackedUser(object):
	def __init__(self, raw_data):
		self._raw = raw_data
		
		if 'lastupd' in raw_data and raw_data['lastupd'] not in (None, -1):
			self._updated = datetime.datetime.now(pytz.utc) - datetime.timedelta(seconds=raw_data['lastupd'])
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
		return self._raw['user']
	
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
	def __init__(self, api_key, uri=STACKPTR_URI):
		self._uri = uri
		self._api_key = api_key

	def _req(self, path, params=None, json=False):
		path = urlparse.urljoin(self._uri, path)
		if params is None:
			response = requests.get(path, params={'apikey': self._api_key})
		else:
			params['apikey'] = self._api_key
			response = requests.post(path, params=params)
		
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
		
		return TrackedUser(r['me']), [TrackedUser(x) for x in r['following']]