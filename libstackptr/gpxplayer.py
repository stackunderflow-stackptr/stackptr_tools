#!/usr/bin/env python
"""
Test program for libstackptr
Copyright 2014 Michael Farrell <http://micolous.id.au>

License: 3-clause BSD, see COPYING
"""

from __future__ import absolute_import
from . import StackPtrClient
from argparse import ArgumentParser, FileType
import gpxpy, datetime, pytz, time, random, requests


def play_gpx(client, gpx_fh):
	gpx = gpxpy.parse(gpx_fh)
	track_seg = gpx.tracks[0].segments[0]
	prev_point = None
	
	points = list(track_seg.points)
	points.sort(key=lambda x: x.time)

	# do the first update
	client.update(points[0].latitude, points[0].longitude)

	start_time = datetime.datetime.now(pytz.utc)
	first_point_time = points[0].time
	offset = start_time - first_point_time
	for point in points[1:]:
		# wait until we're ready
		delta = ((point.time + offset) - datetime.datetime.now(pytz.utc)).total_seconds()
		if delta > 0:
			print 'napping for %.2f second(s)...' % delta
			time.sleep(delta)
		elif delta < 0:
			print 'skipping point, we are %0.2f second(s) late...' % delta
			continue

		try:
			client.update(point.latitude, point.longitude, point.elevation)
			print point
		except requests.exceptions.ConnectionError, e:
			print 'Failure posting update, %r' % e




def main():
	parser = ArgumentParser()

	parser.add_argument('api_key',
		help='API key to use',
		nargs=1
	)

	parser.add_argument('gpx_file',
		help='GPX track file to play, using the first track and first segment in the file.',
		type=FileType('rb'),
		nargs='+'
	)

	parser.add_argument('-s', '--shuffle', action='store_true')

	options = parser.parse_args()

	client = StackPtrClient(options.api_key)
	if options.shuffle:
		random.shuffle(options.gpx_file)

	for f in options.gpx_file:
		print "playing %s" % f
		play_gpx(client, f)


if __name__ == '__main__':
	main()
