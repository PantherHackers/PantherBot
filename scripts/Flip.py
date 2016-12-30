#!/usr/bin/env python
# -*- coding: utf-8 -*-
import upsidedown

#flips text using upsidedown module and has a donger for emohasis
def flip(args):

	toFlip = ''
	if args[0].lower() == "!rage":
		donger = '(ノಠ益ಠ)ノ彡'
		for n in range(2, len(args)):
			toFlip += args[n] + " "
	else:
		donger = '(╯°□°）╯︵'
		if len(args) >= 1:
			for n in range(1, len(args)):
				toFlip += args[n] + " "

	if toFlip == '':
		toFlip = unicode('┻━┻', "utf-8")

	try:
		donger = unicode(donger, "utf-8")
		flippedmsg = upsidedown.transform(toFlip)
		return donger + flippedmsg
	except:
		print "PantherBot:Log:Flip:Error in flip"
		return "Sorry, I can't seem to flip right now, or you gave an invalid argument"
