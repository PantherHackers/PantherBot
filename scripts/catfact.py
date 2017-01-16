#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, json
#returns a random catfact from an api
def catfact(response):
	web_page_contents = urllib2.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read()
	parsed_wbc = json.loads(web_page_contents)
	if "true" in parsed_wbc["success"]:
		return [parsed_wbc["facts"][0]]
	else:
		print "PantherBot:Log:CatFact: Error in catFacts"
		return ["Cat facts can't be returned right now :sob:"]
