#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, json

#pug bombs the chat and destroys this poor bot's soul
def pugbomb(response):

	#gets the number
	x = [int(s) for s in response["text"].split() if s.isdigit()]
	if x[0] > 10:
		x[0] = 10
	u = "http://pugme.herokuapp.com/bomb?count=" + str(x[0])
	m = urllib2.urlopen(u).read()
	m = json.loads(m)
	return m
