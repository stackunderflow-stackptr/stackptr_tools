*****************
API Documentation
*****************

The API endpoint is located at https://stackptr.com/  All REST requests **must** be made with HTTPS.  All URIs in this document are relative to that path.

Access for HTTP is controlled by an API key.  These can be managed in the web interface at https://stackptr.com/api/

When an API call is made, the call will return a number of objects. These objects represent the state updates that resulted from performing that API call.

Most API calls can be made via either the HTTPS or WAMP endpoints (TODO: document which ones, and make the ones that should be available usable on both)

In addition to the API calls, you can also connect via the WAMP transport and receive location updates pushed directly to your client instead of polling the ``/users`` endpoint repeatedly.

It is recommended that the application simply implement generic parsers for each type of message, instead of for each API call, as some endpoints return the same message types.


Format specifics
================

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

   Note: Currently returns the username that the API key is for, but this endpoint is likely to be removed and replaced with something better.


CSRF
====

.. function:: GET /csrf

	Returns a CSRF token. All requests made with API keys are exempt from CSRF checks, so you'll only need this to POST to /login and create an API key for your app yourself.
	
	Note: This will be replaced with something better and this function will be removed in future.

Update location
===============

.. function:: POST /update

   Updates your current location, using (ideally) data from your GPS receiver.  Do not report a location if your location is not known.

   :param float lat: Your current latitude.
   :param float lon: Your current longitude.
   :param float alt: Your current altitude, in metres, if known.  Omit parameter if unknown.
   :param float hdg: Your current heading, in degrees, if known.  Omit parameter if unknown.
   :param float spd: Your current speed, in metres/second, if known.  Omit parameter if unknown.
   :param string ext: A JSON dict of additional optional information.

   In response, the server will send back ``OK``. Anything else indicates an error.

.. class:: Extra
	
   :param string bat: Battery life between 0.0 and 1.0.
   :param string bst: Battery status: ``charging``, ``full`` or ``discharging``.
   :param string prov: Location provider name.
   
   Arbitrary other parameters may be included - more will be defined later.

WAMP Connections
==========

.. function:: POST /ws_uid

   Returns your current UID (i.e. the UID that you should authenticate to the WAMP server as).

.. function:: POST /ws_token
   
   Returns a token used in the challenge/response WAMP authentication.


User Data
==========

.. function:: GET /users

   Gets a list of users on stackptr and their current locations.
   
   The response is encoded as JSON.
   
   This is returned as a list of :class:`MessageItem`.

.. class:: MessageItem

   Structure for storing messages sent over the wire in ``/users`` calls or WAMP calls.
   
   .. data:: type
   
      The type of message being sent.  This is one of the message types.

   .. data:: data
   
      Types of object:
   
   ``user-me``
      A :class:`TrackedUser` for your user.
   
   ``user``
      An array of :class:`TrackedUser` for users that you watch.
   
   ``user-pending``
      An array of users that you want to follow but they have not accepted. (FIXME: format)
   
   ``user-request``
      An array of users that want to follow you but you have not accepted. (FIXME: format)


.. class:: TrackedUser

   Structure for passing location information about tracked users in the StackPtr API.
   
   :param array loc: Array containing ``[latitude, longitude]`` containing the current location of the user.
   :param string username: The username of the tracked user.
   :param string icon: URI of the avatar for the user.
   :param string lastupd: Time of last update, in seconds since UNIX epoch in UTC.
   :param string alt: Altitude of the user in metres above sea level.
   :param string extra: A dictionary of :class:`Extra` information about the user.
   :param string hdg: Heading of the user.
   :param string id: User ID of the user.
   :param string spd: Speed of the user


.. function:: GET /lochist

User Management
==========

.. function:: POST /acceptuser

.. function:: POST /adduser

.. function:: POST /deluser


Group Data
==========

.. function:: GET /grouplist

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
	
