#!/usr/bin/env python
"""
Test program for libstackptr
Copyright 2014 Michael Farrell <http://micolous.id.au>

License: GPLv3+, see COPYING
"""

from __future__ import absolute_import
from . import StackPtrClient
from argparse import ArgumentParser
import pprint


def main():
	parser = ArgumentParser()
	
	parser.add_argument('api_key',
		help='API key to use',
		nargs=1
	)
	
	parser.add_argument('-u', '--uri',
		help='URI of stackptr server.'
	)

	options = parser.parse_args()
	
	client = StackPtrClient(options.api_key, options.uri)
	me, following = client.users()
	
	print 'My location:'
	pprint.pprint(me)
	print ''
	print 'Following:'
	pprint.pprint(following)


if __name__ == '__main__':
	main()
