#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient
from scripts import Help, CatFacts, Flip, GiveFortune, Coin, Log, Pugbomb, Unflip
import os, sys, codecs, websocket, thread, datetime, json, urllib2, random, upsidedown, logging

#initialize basic logging to see errors more easily
#logger = logging.getLogger('root')
#FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
#logging.basicConfig(format=FORMAT)
#logger.setLevel(logging.DEBUG)

#Get Token from local system environment variables
t = os.environ['SLACK_API_TOKEN']

#CUSTOM VARIABLES
BOT_NAME = 'PantherBot'
BOT_ICON_URL = 'https://www.iconexperience.com/_img/g_collection_png/standard/512x512/robot.png'
#contains user IDs for those allowed to run $ commands
ADMIN = ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"]

#Global Variables
global LOG
LOG = False
global LOGC
LOGC = []

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
		#If $log has been set to true it will save all spoken messages.
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

		#Riyan's denial
		if "U0LJJ7413" in response["user"]:
			if response["text"][:1] in ["!", "$", "Hey PantherBot"]:
				rMsg(response, "No.")
				return

		#Checks if message starts with an exclamation point, and does the respective task
		elif response["text"][:1] == "!":
			#put all ! command parameters into an array
			words = response["text"].split()
			#Command logic
			if words[0].lower() == "!catfact":
				rMsg(response, CatFacts.catFacts(response))
				return
			if words[0].lower() == "!coin":
				rMsg(response, Coin.coin(response))
				return
			if words[0].lower() == "!fortune":
				rMsg(response, GiveFortune.giveFortune(response))
				return
			if words[0].lower() == "!pugbomb":
				rMsg(response, Pugbomb.pugbomb(response))
				return
			if words[0].lower() == "!flip" or words[0].lower() == "!rage":
				rMsg(response, Flip.flip(response, words))
				return
			if words[0].lower() == "!unflip":
				rMsg(response, Unflip.unflip(response, words))
				return
			if words[0].lower() == "!help":
				rMsg(response, Help.help(response))
				return
		#Checks for a log command
		elif response["text"][:1] == "$":
			words = response["text"].split()
			#Command logic
			if words[0].lower() == "$log":
				if response["user"] in ADMIN:
					print "PantherBot:LOG:Approved User called $log"
					Log.log(response, words)
					return

		#If not an ! or $, checks if it should respond to another message format, like a greeting
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

#necessary shenanigans
if __name__ == "__main__":
	#Checks if the system's encoding type is utf-8 and changes it to utf-8 if it isnt (its not on Windows by default)
	if sys.stdout.encoding != 'utf-8':
		sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
	if sys.stderr.encoding != 'utf-8':
		sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')
    #websocket.enableTrace(True)
	ws = websocket.WebSocketApp(test["url"],
							on_message = on_message,
							on_error = on_error,
							on_close = on_close)
	#ws.on_open = on_open
	ws.run_forever()
