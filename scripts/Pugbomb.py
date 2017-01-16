#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, json

#pug bombs the chat and destroys this poor bot's soul
def pugbomb(response, args):

	#gets the number
	#num = [int(s) for s in response["text"].split() if s.isdigit()]
	num = int(args[0])
	if num > 10:
		num = 10
	url = "http://pugme.herokuapp.com/bomb?count=" + str(num)
	json_r = urllib2.urlopen(url).read()
	json_p = json.loads(json_r)
	l = []
	for x in json_p["pugs"]:
		l.append(x)
	return l
