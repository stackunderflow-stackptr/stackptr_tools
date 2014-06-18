#!/usr/bin/env python
"""
Test program for libstackptr
Copyright 2014 Michael Farrell <http://micolous.id.au>

License: 3-clause BSD, see COPYING
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
	
	options = parser.parse_args()
	
	client = StackPtrClient(options.api_key)
	me, following = client.users()
	
	print 'My location:'
	pprint.pprint(me)
	print ''
	print 'Following:'
	pprint.pprint(following)


if __name__ == '__main__':
	main()
