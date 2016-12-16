#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2

#returns a random "fortune"
def giveFortune(response):
	try:
		#get fortune
		fortune = urllib2.urlopen("http://www.fortunefortoday.com/getfortuneonly.php").read()
	except:
		fortune = "Unable to reach fortune telling api"
		print "PantherBot LOG:Fortune:Error in receiving fortune"

	#make api call
	return fortune