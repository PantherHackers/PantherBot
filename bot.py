#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient
import os
import sys
import codecs
import websocket
import thread
import time
import datetime
import json
import urllib2
import random
import upsidedown
import logging

#initialize basic logging to see errors more easily
logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

#Get Token from local system environment variables
t = os.environ['SLACK_API_TOKEN']

#Global Variables
BOT_NAME = 'PantherBot'
BOT_ICON_URL = 'https://www.iconexperience.com/_img/g_collection_png/standard/512x512/robot.png'
global LOG
LOG = False
global LOGC
LOGC = []
ADMIN = ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"]

#initiates the SlackClient connection
sc = SlackClient(t)

#initiates connection to the server based on the token
test = sc.api_call(
	"rtm.start",
	token = t
)

#function that is called whenever there is an event, including status changes, join messages, typing status, emoji reactions, everything
def on_message(ws, message):
	#converts to usable string format
	s = message.encode('ascii')

	#converts to JSON so we can parse through it easier
	response = json.loads(s)
	print "PantherBot LOG:" + response["type"]

	#Checks if the event type returned by Slack is a message
	if "message" == response["type"]:
		global LOG, LOGC
		if LOG == True and response["channel"] in LOGC:
			filename = "logs/" + response["channel"] + " " + str(datetime.date.today()) + ".txt"
			d0 = sc.api_call(
				"users.info",
				user = response["user"]
			)
			u = d0["user"]["profile"]["first_name"] + " " + d0["user"]["profile"]["last_name"]
			script_dir = os.path.dirname(__file__)
			adir = os.path.join(script_dir, filename)
			if os.path.isfile(adir) == True:
				target = open(adir, "a")
			else:
				target = open(adir, "w+")
			target.write(u + "\n")
			target.write(response["text"] + " [")
			target.write(response["ts"] + "]\n\n")
			target.close()
		#Checks if message starts with an exclamation point, and does the respective task
		if response["text"][:1] == "!":
			#put all ! command parameters into an array
			words = response["text"].split()
			#Command logic
			if words[0].lower() == "!catfact":
				catFacts(response)
				return
			if words[0].lower() == "!coin":
				coin(response)
				return
			if words[0].lower() == "!fortune":
				giveFortune(response)
				return
			if words[0].lower() == "!pugbomb":
				pugbomb(response)
				return
			if words[0].lower() == "!flip" or words[0].lower() == "!rage":
				flip(response, words)
				return
			if words[0].lower() == "!unflip":
				unflip(response, words)
				return
			if words[0].lower() == "!help":
				help(response)
				return
		elif response["text"][:1] == "$":
			words = response["text"].split()
			#Command logic
			if words[0].lower() == "$log":
				if response["user"] in ADMIN:
					print "PantherBot:LOG:Approved User called $log"
					log(response, words)
					return
		#If not an !, checks if it should respond to another message format, like a greeting
		elif "Hey PantherBot" in response["text"]:
			#returns user info that said hey
			d0 = sc.api_call(
				"users.info",
				user = response["user"]
			)
			print "PantherBot LOG:Greeting:We did it reddit"
			try:
				#attempts to send a message to Slack, this one is the only one that needs this try thing so far, no clue why
				rMsg(response, "Hello, " + d0["user"]["profile"]["first_name"] + "! :tada:")
			except:
				print "PantherBot LOG:Greeting:Error in response"

def on_error(ws, error):
	print error

def on_close(ws):
	print "### closed ###"

#send a response message (sends to same channel as command was issued)
def rMsg(response, text):
	sc.api_call(
		"chat.postMessage",
		channel=response["channel"],
		text=text,
		username=BOT_NAME,
		icon_url=BOT_ICON_URL
	)

#scripts

#help script that details the list of commands
def help(response):
	text = "PantherBot works by prefacing commands with \"!\"\n"
	text = text + "Commands:\n"
	text = text + "```!help\n"
	text = text + "!coin\n"
	text = text + "!fortune\n"
	text = text + "!flip <String>\n"
	text = text + "!catfact\n"
	text = text + "!pugbomb <num>\n"
	text = text + "\"Hey PantherBot\"```\n"
	text = text + "Try saying `Hey PantherBot` or `!coin`"
	rMsg(response, text)

#returns a random catfact from an api
def catFacts(response):
	m = urllib2.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read()
	m = json.loads(m)
	if "true" in m["success"]:
		rMsg(response, m["facts"][0])
	else:
		print "PantherBot LOG:CatFact: Error in catFacts"
		rMsg(response, "Cat facts can't be returned right now :sob:")

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
		rMsg(response, donger + flippedmsg)
	except:
		print "PantherBot LOG:Flip:Error in flip"
		rMsg(response, "Sorry, I can't seem to flip right now")

#"unflips" text
def unflip(response, words):
	toUnFlip = ''
	for n in range(1, len(words)):
		toUnFlip += words[n] + " "

	if toUnFlip == "":
		toUnFlip = unicode('┬──┬', "utf-8")

	try:
		donger = "ノ( º _ ºノ)"
		donger = unicode(donger, "utf-8")
		rMsg(response, toUnFlip + donger)
	except:
		print "PantherBot LOG:Flip:Error in flip"
		rMsg(response, "Sorry, I can't seem to unflip right now")

#flips a coin
def coin(response):
	l = ["Heads", "Tails"]
	m = random.randrange(0,2)
	rMsg(response, l[m])

#returns a random "fortune"
def giveFortune(response):
	try:
		#get fortune
		fortune = urllib2.urlopen("http://www.fortunefortoday.com/getfortuneonly.php").read()
	except:
		fortune = "Unable to reach fortune telling api"
		print "PantherBot LOG:Fortune:Error in receiving fortune"

	#make api call
	rMsg(response, fortune)

#pug bombs the chat and destroys this poor bot's soul
def pugbomb(response):
	x = [int(s) for s in response["text"].split() if s.isdigit()]
	u = "http://pugme.herokuapp.com/bomb?count=" + str(x[0])
	m = urllib2.urlopen(u).read()
	m = json.loads(m)
	for s in m["pugs"]:
		rMsg(response, s)

#enables logging of messages on a channel/channels, storing the logs sorted by channel by day in the format "channelID Y-M-D"
def log(response, words):
	if "true" == words[1].lower():
		global LOGC
		global LOG
		LOG = True
		if len(words) > 2:
			print "PantherBot:LOG:List of channels to log gathered"
			i = 2
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
						found = True
						break
				#Same as above
				for p in p0["groups"]:
					if p["name"].lower() == words[w].lower():
						LOGC.append(str(p["id"]))
						found = True
						break
				#If no channel is found by that name, increases the offset by one (skips an argument, essentially)
				if found == False:
					i = i + 1
		else:
			print "PantherBot:LOG:No Channels listed to log, logging channel $log was called in"
			LOGC.append(str(response["channel"]))
		return
	if "false" == words[1].lower():
		print "PantherBot:LOG:Disabling logging"
		global LOG
		LOG = False
		DUMMY = []
		LOGC = DUMMY
		return

#necessary shenanigans
if __name__ == "__main__":
	#Checks if the system's encoding type is utf-8 and changes it to utf-8 if it isnt (its not on Windows by default)
	if sys.stdout.encoding != 'utf-8':
		sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
	if sys.stderr.encoding != 'utf-8':
		sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')
	logging.basicConfig()
    #websocket.enableTrace(True)
	ws = websocket.WebSocketApp(test["url"],
							on_message = on_message,
							on_error = on_error,
							on_close = on_close)
	#ws.on_open = on_open
	ws.run_forever()
