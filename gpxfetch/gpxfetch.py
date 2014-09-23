#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import os
import bz2

def fetch(tag):
	page = 1
	while True:		
		url = "https://www.openstreetmap.org/traces/tag/%s/page/%i" % (tag, page)
		print "fetching page %i for tag %s" % (page, tag)
		r = requests.get(url)
		res = r.text
		
		traces = []
		
		soup = BeautifulSoup(res)
		table = soup.find(id="trace_list")
		table = table.find("tbody")
		for item in table:
			td = item.find("td")
			if td != -1:
				td2 = td.find("a")
				if td2:
					traces.append(td2.get("href"))
		
		traces2 = [tr.split("/")[-1] for tr in traces]
		
		count = len(traces)
		print "got %i tracks" % count
		if count == 0:
			return
		
		if not os.path.exists("output"):
			os.mkdir("output")
		
		for trace in traces2:
			filename = trace + ".gpx"
			if os.path.exists(os.path.join("output",filename)):
				print "already done: " + filename
				continue
			print "fetching: " + filename
			r = requests.get("https://www.openstreetmap.org/trace/%s/data" % trace)
			if r.status_code == 200:
				print "successful"
				f = open(os.path.join("output/",filename), 'w')
				res = bz2.decompress(r.content)
				f.write(res)
				f.close()
			else:
				print "failed"
		
		page += 1

fetch("adelaide")


