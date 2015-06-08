#!/usr/bin/env python
"""
GPSd client for libstackptr
Copyright 2014-2015 Michael Farrell <http://micolous.id.au>

License: GPLv3+, see COPYING
"""

from __future__ import absolute_import
from . import StackPtrClient
from argparse import ArgumentParser, FileType
import datetime, random, requests, gps, isodate, sys


def main():
	parser = ArgumentParser()

	parser.add_argument('api_key',
		help='API key to use',
		nargs=1
	)

	parser.add_argument('-u', '--uri',
		help='URI of stackptr server.'
	)

	parser.add_argument('-U', '--update-freq',
		type=int,
		default=10,
		help='Number of seconds to wait between location updates being sent to the server. [default: %(default)s]'
	)

	parser.add_argument('-c', '--gps-clock',
		action='store_true',
		help='If set, the program will use the GPS clock as the source of truth for update frequencies. Otherwise, the system clock will be used instead. When there is a flood of reports, this will cause an update frequency higher than "update-freq" value in real-time, but may work better on systems with bad clock sources.'
	)

	options = parser.parse_args()

	client = StackPtrClient(options.api_key, options.uri)
	last_ts = None
	gps_client = gps.gps()
	gps_client.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
	freq = datetime.timedelta(seconds=options.update_freq)

	while True:
		report = gps_client.next()
		if report['class'] == 'TPV' and report['mode'] >= 2 and 'lat' in report and 'lon' in report:
			# We have a real fix data!
			if options.gps_clock:
				report_ts = isodate.parse_datetime(report['time'])
			else:
				report_ts = datetime.datetime.utcnow()

			if last_ts is None or (report_ts - last_ts) > freq:
				last_ts = report_ts

				# Send a report!
				alt = report.get('alt', 0)
				heading = report.get('track', -1)
				speed = report.get('speed', -1)
				client.update(report['lat'], report['lon'], alt, heading, speed)
				print '\nUpdated: %0.6f,%0.6f %dm %d° %dm/s' % (report['lat'], report['lon'], alt, heading, speed)
			else:
				sys.stdout.write('.')
				sys.stdout.flush()

if __name__ == '__main__':
	main()

