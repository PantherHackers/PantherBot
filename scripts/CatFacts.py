#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, json
#returns a random catfact from an api
def catFacts(response):
	m = urllib2.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read()
	m = json.loads(m)
	if "true" in m["success"]:
		return m["facts"][0]
	else:
		print "PantherBot LOG:CatFact: Error in catFacts"
		return "Cat facts can't be returned right now :sob:"
