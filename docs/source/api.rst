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

Test endpoints
=============

.. function:: POST /uid

   Tests connectivity and authentication to the stackptr API.
   
   Useful to see if the API key provided to your app is correct.

   Returns a JSON dictionary consisting of:

   :param int id: Your numerical uid
   :param string username: Your username
   :param string icon: The user's gravatar (in 256x256).

CSRF
====

.. function:: GET /csrf

	Returns a CSRF token. All requests made with API keys are exempt from CSRF checks, so you will not usually need this.

   The Android app uses this to POST to /login, get a session and create an API key automatically for you.

   The Web UI uses this before the post to /ws_token as the CSRF token obtained when the page first loaded may be expired if the websocket connection drops and reconnects a long time after the page first loaded.

   This endpoint does not support CORS for obvious reasons.
	
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

.. function:: GET /users | com.stackptr.api.userList

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
   :param string icon: URI of the avatar for the user (64x64).
   :param string lastupd: Time of last update, in seconds since UNIX epoch in UTC.
   :param string alt: Altitude of the user in metres above sea level.
   :param string extra: A dictionary of :class:`Extra` information about the user.
   :param string hdg: Heading of the user.
   :param string id: User ID of the user.
   :param string spd: Speed of the user


.. function:: GET /lochist | com.stackptr.api.lochist

   Get the specified user's location history.

   :param int uid: The user you want to get the location history of. If not specified, will fetch your own.

   Returns a message of type ``lochist``, with the data containing ``id`` and ``lochist``. ``lochist`` in this is an array of dictionaries containing ``lat`` and ``lng`` objects. This array is ordered from least recent to most recent.

   Returns "Permission Denied" if you fetch a user that is not in your user list.

   Your application should fetch this only once upon first load, and then append to this list itself instead of repeatedly fetching this endpoint.



User Management
===============

.. function:: POST /adduser | com.stackptr.api.addUser
   
   Request permission to see a user's location. Grants them permission to see yours.

   :param int user: Username or email address of user to add

.. function:: POST /acceptuser | com.stackptr.api.acceptUser

   Accept another user's add request

   :param int uid: User ID to accept

.. function:: POST /deluser | com.stackptr.api.delUser

   Delete a user from your contact list and you from theirs

   :param int uid: User ID to delete


Group Data
==========

.. function:: GET /grouplist | com.stackptr.api.groupList

   Get the list of groups the user is in

.. class:: Group

   Structure for grouplist responses

   .. data:: name

      Name of the group

   .. data:: id
      
      ID of the group

   .. data:: description

      Description of the group

   .. data:: status

      0 = open to join via group discovery
      1 = require owner approval to join

   .. data:: members

      List of members in the group, containing username, icon, id, role

      Role:
      1 = member
      2 = administrator

.. function:: GET /groupdiscover | com.stackptr.api.groupDiscover
   
   Gets a list of groups that are open for public discovery and that you are not already in.

.. function:: POST /creategroup | com.stackptr.api.createGroup

   Create a new group.

   :param string name: Name for group
   :param string description: Description for group
   :param string status: 0 if others can discover group, 1 for private group.

.. function:: POST /joingroup | com.stackptr.api.joinGroup

   :param string gid: ID of group to join

.. function:: POST /leavegroup | com.stackptr.api.leaveGroup

   :param string gid: ID of group to leave. You can't leave a group that you are the sole admin of.

.. function:: POST /deletegroup | com.stackptr.api.deleteGroup

   :param string gid: ID of group to delete. You must be an admin.

.. function:: POST /updategroup | com.stackptr.api.updateGroup

   :param string name: Name for group
   :param string description: Description for group
   :param string status: 0 if others can discover group, 1 for private group.
   :param string gid: Group ID

.. function:: POST /groupusermod | com.stackptr.api.groupUserMod
 
   :param string gid: ID of group
   :param string uid: ID of user
   :param string user: Alternatively specify user by username or email.
   :param string role: New role for user. 0 to delete user, 1 to demote to regular user, 2 to promote to admin.

.. function:: POST /groupdata | com.stackptr.api.groupData
	
	Gets a dict of the data (placemarks etc) for a group. The key for the dict is the object's ID (unique across all groups) and the value is a :class:`GroupData` item.
	
	:param int gid: The group ID you want data for.
	
.. class:: GroupData

	Structure representing an object in a group like a placemark, line or polygon.
	
	.. data:: name
	
	Name of the item.
	
	.. data:: owner
	
	Username of the owner / creator of the object.
	
	.. data:: json
	
	GeoJSON representing the object as it is to be drawn on the map.

.. function:: POST /addfeature | com.stackptr.api.addFeature
	
	Adds a new item to the group.
	
	:param string name: Name for object
   :param string group: Group id to add feature to
	:param string geojson: GeoJSON representation of the object

.. function:: POST /delfeature | com.stackptr.api.deleteFeature
	
	Deletes an item in the group.
	
	:param int fid: ID of object to delete

.. function:: POST /editfeature | com.stackptr.api.editFeature

   Edits the geometry of an item in the group.
   
   :param int fid: ID of object to rename
   :param string gjson: new geoJSON of object

.. function:: POST /renamefeature | com.stackptr.api.renameFeature

	Renames an item in the group.
	
	:param int fid: ID of object to rename
	:param string name: New name for object
	
.. function::  | com.stackptr.api.setSharedToGroup

   Start or stop sharing to a group.

   :param string gid: ID of group
   :param string share: 1 to start sharing to group, 0 to stop sharing

.. function::  | com.stackptr.api.sharedGroupLocs
   
   Get the locations of group members sharing to the group.

   :param string gid: ID of group

