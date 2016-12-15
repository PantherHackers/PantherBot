#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient
import os
import sys
import codecs
import websocket
import thread
import time
import json
import urllib2
import random
import upsidedown

#Get Token from local system environment variables
t = os.environ['SLACK_API_TOKEN']

BOT_NAME = 'PantherBot'
BOT_ICON_URL = 'https://www.iconexperience.com/_img/g_collection_png/standard/512x512/robot.png'

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
			if words[0].lower() == "!flip":
				flip(response, words)
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
	try:
		toFlip = ""
		donger = "(┛ಠДಠ)┛彡┻━┻ "
		donger = unicode(donger, "utf-8")
		for n in range(1,len(words)):
			toFlip = toFlip + words[n] + " "
		flippedmsg = upsidedown.transform(toFlip)
		rMsg(response, donger + flippedmsg)
	except:
		print "PantherBot LOG:Flip:Error in flip"
		rMsg(response, "Sorry, I can't seem to flip right now")

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

#Checks if the system's encoding type is utf-8 and changes it to utf-8 if it isnt (its not on Windows by default)
if sys.stdout.encoding != 'utf-8':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
if sys.stderr.encoding != 'utf-8':
  sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')

#necessary shenanigans
if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(test["url"],
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    #ws.on_open = on_open
    ws.run_forever()
	

