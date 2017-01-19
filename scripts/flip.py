#!/usr/bin/env python
# -*- coding: utf-8 -*-
import upsidedown

#flips text using upsidedown module and has a donger for emohasis
def flip(response, args=[]):
	toFlip = ''
	donger = '(╯°□°)╯︵'
	if len(args) >= 0:
		for n in range(0, len(args)):
			toFlip += args[n] + " "

	if toFlip == '':
		toFlip = unicode('┻━┻', "utf-8")

	try:
		donger = unicode(donger, "utf-8")
		flippedmsg = upsidedown.transform(toFlip)
		return [donger + flippedmsg]
	except:
		print "PantherBot:Log:Flip:Error in flip"
		return ["Sorry, I can't seem to flip right now, or you gave an invalid argument"]
