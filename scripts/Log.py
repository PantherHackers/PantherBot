#!/usr/bin/env python
# -*- coding: utf-8 -*-

#enables logging of messages on a channel/channels, storing the logs sorted by channel by day in the format "channelID Y-M-D"
def log(response, words):
	if "true" == words[1].lower():
		global LOGC
		global LOG
		LOG = True
		if len(words) > 2:
			print "PantherBot:LOG:List of channels to log gathered"

			#obtains list of public channels PB is in
			c0 = sc.api_call(
				"channels.list",
				exclude_archived = 1
			)
			#obtains list of private channels PB is in
			p0 = sc.api_call(
				"groups.list",
				exclude_archived = 1
			)
			#Goes through the arguments after true
			print "PantherBot:LOG:Parsing list of channels to log"
			for w in range(2, len(words)):
				#Flag to keep track of whether argument channel was found
				found = False
				#goes through the list of public channels, if found by name, its ID is added to the list of channels to go monitor
				for c in c0["channels"]:
					if c["name"].lower() == words[w].lower():
						LOGC.append(str(c["id"]))
						break
				#Same as above
				for p in p0["groups"]:
					if p["name"].lower() == words[w].lower():
						LOGC.append(str(p["id"]))
						break

		else:
			print "PantherBot:LOG:No Channels listed to log, logging channel $log was called in"
			LOGC.append(str(response["channel"]))
		return
	if "false" == words[1].lower():
		print "PantherBot:LOG:Disabling logging"
		global LOG
		global LOGC
		LOG = False
		DUMMY = []
		LOGC = DUMMY
		return
