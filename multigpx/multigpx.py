#!/usr/bin/env python

import sys, os
sys.path.append("../")
import libstackptr, libstackptr.gpxplayer
from multiprocessing import Process
import json
import random
import time

def startgpx(apikey, directory):
	client = libstackptr.StackPtrClient(apikey, "http://localhost/")
	while True:
		gpxname = random.choice(directory)
		print "using %s" % gpxname
		f = open(gpxname, 'r')
		try:
			libstackptr.gpxplayer.play_gpx(client, f)
		except:
			continue
		finally:
			f.close()

if __name__ == '__main__':
	f = open(sys.argv[1], 'r')
	userlist = json.loads(f.read())
	#print userlist
	
	gpxlist = os.listdir(sys.argv[2])
	gpxlist = filter(lambda a: a.endswith(".gpx"), gpxlist)
	gpxlist = map(lambda a: os.path.join(sys.argv[2], a), gpxlist)
	#print gpxlist
	
	for user in userlist:
		p = Process(target=startgpx, args=(user['apikey'],gpxlist))
		p.daemon = True
		p.start()
	
	while True:
		time.sleep(30)