#!/usr/bin/env python
# -*- coding: utf-8 -*-
import upsidedown

#flips text using upsidedown module
def flip(response, words):
	toFlip = ''
	if words[0].lower() == "!rage":
		donger = '(ノಠ益ಠ)ノ彡'
		for n in range(2, len(words)):
			toFlip += words[n] + " "
	else:
		donger = '(╯°□°）╯︵'
		if len(words) >= 1:
			for n in range(1, len(words)):
				toFlip += words[n] + " "

	if toFlip == '':
		toFlip = unicode('┻━┻', "utf-8")

	try:
		donger = unicode(donger, "utf-8")
		flippedmsg = upsidedown.transform(toFlip)
		return donger + flippedmsg
	except:
		print "PantherBot LOG:Flip:Error in flip"
		return "Sorry, I can't seem to flip right now"
