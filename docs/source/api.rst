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

Update location
===============

.. function:: POST /update

   Updates your current location, using (ideally) data from your GPS receiver.  Do not report a location if your location is not known.

   :param float lat: Your current latitude.
   :param float lon: Your current longitude.
   :param float alt: Your current altitude, if known.  Report ``0`` if unknown.
   :param float hdg: Your current heading, if known.  Report ``-1``, and do not report speed, if heading is unknown.
   :param float spd: Your current speed, if unknown.  Report ``-1`` if unknown or if heading is unknown.

   In response, the server will send your latitude and longitude encoded as follows, but do not expect a response::

      lat: -34.0; lon: 137.0

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
   
      Number of seconds ago that the location was recorded.
