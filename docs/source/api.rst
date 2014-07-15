*****************
API Documentation
*****************

The API endpoint is located at https://stackptr.com/  All requests **must** be made with HTTPS.  All URIs in this document are relative to that path.

Access is controlled by an API key.  These can be managed in the web interface at https://stackptr.com/api/

API keys are passed with the GET or POST parameter ``apikey``.  All calls require this key unless otherwise specified.

Latitude and longitude are passed using the WGS84 CRS, and encoded as a decimal number of degrees with a precision of up to 64 bit.  Southern latitudes are indicated as negative numbers, western longitudes are indicated as negative.

Altitude is reported in metres above sea level.

Heading is passed in degrees, with north being 0/360 degrees.

Speed is reported in metres per second at ground level.

Test endpoint
=============

.. function:: GET /test

   Tests connectivity and authentication to the stackptr API.
   
   Useful to see if the API key provided to your app is correct.

   Returns the username that the API key is for, but what exactly is returned will likely change.


CSRF
====

.. function:: GET /csrf

	Returns a CSRF token. All requests made with API keys are exempt from CSRF checks, so you'll only need this to POST to /login and create an API key for your app yourself.
	
	This is not the recommended way of doing it, and this function may be removed in future.

Update location
===============

.. function:: POST /update

   Updates your current location, using (ideally) data from your GPS receiver.  Do not report a location if your location is not known.

   :param float lat: Your current latitude.
   :param float lon: Your current longitude.
   :param float alt: Your current altitude, if known.  Omit parameter if unknown.
   :param float hdg: Your current heading, if known.  Omit parameter if unknown.
   :param float spd: Your current speed, if known.  Omit parameter if unknown.
   :param string ext: A JSON dict of additional optional information.

   In response, the server will send back ``OK``. Anything else indicates an error.

.. class:: Extra
	
   :param string bat: Battery life between 0.0 and 1.0.
   :param string bst: Battery status: ``charging``, ``full`` or ``discharging``.
   :param string prov: Location provider name.

Users list
==========

.. function:: GET /users

   Gets a list of users on stackptr and their current locations.
   
   The response is encoded as JSON.
   
   ``response['me']``
      A :class:`TrackedUser` for your user.
   
   ``response['following']``
      An array of :class:`TrackedUser` for users that you watch.


.. class:: TrackedUser

   Structure for passing location information about tracked users in the StackPtr API.
   
   .. data:: loc
   
      Array containing ``[latitude, longitude]`` containing the current location of the user.
   
   .. data:: user
   
      The username of the tracked user.
   
   .. data:: icon
   
      URI of the avatar for the user.
   
   .. data:: lastupd
   
      Time of last update, in seconds since UNIX epoch in UTC.

Group Data
==========

.. function:: POST /groupdata
	
	Gets a dict of the data (placemarks etc) for a group. The key for the dict is the object's ID (unique across all groups) and the value is a :class:`GroupData` item.
	
	:param int group: The group ID you want data for (not implemented yet, there is only one group)
	
.. class:: GroupData

	Structure representing an object in a group like a placemark, line or polygon.
	
	.. data:: name
	
	Name of the item.
	
	.. data:: owner
	
	Username of the owner / creator of the object.
	
	.. data:: json
	
	GeoJSON representing the object as it is to be drawn on the map.

.. function:: POST /addfeature
	
	Adds a new item to the group.
	
	:param string name: Name for object (not implemented yet, defaults to untitled)
	:param string geojson: GeoJSON representation of the object

.. function:: POST /delfeature
	
	Deletes an item in the group.
	
	:param int id: ID of object to delete

.. function:: POST /renamefeature

	Renames an item in the group.
	
	:param int id: ID of object to rename
	:param string name: New name for object
	
