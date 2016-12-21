#!/usr/bin/env python
# -*- coding: utf-8 -*-

#"unflips" text
def unflip(words):
	toUnFlip = ''
	for n in range(1, len(words)):
		toUnFlip += words[n] + " "

	if toUnFlip == "":
		toUnFlip = unicode('┬──┬', "utf-8")

	try:
		donger = "ノ( º _ ºノ)"
		donger = unicode(donger, "utf-8")
		return toUnFlip + donger
	except:
		print "PantherBot LOG:Flip:Error in flip"
		return "Sorry, I can't seem to unflip right now"
