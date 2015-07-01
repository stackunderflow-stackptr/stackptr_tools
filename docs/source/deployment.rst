**********
Deployment
**********

Serving
=======

The StackPtr application has five different components.

Static Files
------------
CSS/JS/Images and other resources served straight from the filesystem.

These files are located in /static and should also be served up on /static/ on the HTTP server.

REST API / Pages
----------------
This part is written in Flask and contains the signup, login, API key management and main map view, as well as the REST API.

It is a WSGI application contained within stackptr.py that imports some shared functionality from stackptr_core.py.

The HTML templates are in /templates.

WAMP application
----------------
This part is a Crossbar application that implements the real-time WAMP API.

It is located in stackptr_realtime.py.

SQL Server
----------
Set the path to the database in stackptr.conf, under the database section.
Example: ::
	[database]
	uri=postgresql://username:password@host/dbname

There exists a full set of Alembic migrations for the database in /migrations that can be used to create the database with the correct schema.

TODO: command? :)

Tile Server
-----------
StackPtr comes pre-configured to use the StackTiles server as well as MapQuest's OSM server.

Your install of StackPtr is allowed to use the StackTiles server as long as it doesn't put too much load on it.

If you're planning on doing that, email the dev team first :)

Development
===========
For development purposes, it's easiest to serve the static files, WAMP application and realtime componets from within Crossbar.

An example configuration for Crossbar in this configuration is located at 

TODO: command to fire this up? location of this file?

Deployment
==========
For deployment purposes, the recommended configuration is to use nginx as the frontend server.

Nginx is set up to serve the static files directly.

Behind nginx, uwsgi is used to run the WSGI application component. 

Crossbar still runs, but it has a static webserver configured on / serving from /var/empty, and the webserver on /ws. This is then proxied through by nginx.

The reason for this slightly odd configuration is that Crossbar cannot be configured to have the webserver on /, or to not run with a static webserver.

todo: instructions on setting this up on a debian-based system