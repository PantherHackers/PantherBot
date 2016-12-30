#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Slack imports
from slackclient import SlackClient
#Google imports
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
#Other imports
from scripts import Help, CatFacts, Flip, GiveFortune, Coin, Pugbomb, Unflip, Calendar, TaskMe
import os, sys, codecs, websocket, datetime, json, logging

#Custom Variables
BOT_NAME = 'PantherBot' #Set to whatever you would like the Bot to post his name as in Slack
BOT_ICON_URL = 'http://i.imgur.com/QKaLCX7.png' #Set to change whatever the profile picture is when the Bot posts a message
SLACK = True #Set to False to disable connecting to the Slack RTM API... for whatever reason
GOOGLECAL = False #Set to False to disable connecting and enabling the Google Calendar API integration
LOGGER = False #Set to True to get "detailed" error messages in the console. These error messages can vary from very helpful to utterly useless
GOOGLECALSECRET = "PantherBot-test.json" #Can make this a system environment variable if you really want to be careful
NEWUSERGREETING = True #Set to True to send users that join the Slack Team a message (GREETING), appended with a link (LINK) (used for whatever you want, in our case, a "How to Use Slack" document)
LINK = "https://test.link.pantherhackers.com" #link to be appended to GREETING
GREETING = "Greetings newcomer! This is your friendly neighborhood PantherBot, a bot created by your fellow members of PantherHackers! We just wanted to say hello, and welcome you to the family! If Slack seems intimidating, have no fear! If you've ever messed with the likes of Discord, it is a lot like that. If you haven't messed with that either, again, no worries.\nTo get started, you have your default channels on the left (expand the menu by tapping the Panther icon in the top left if you are on mobile). To join more channels, click/tap on the plus button next to \"CHANNELS\" and you'll be well on your way.\nIf you are interested to learn more about Slack, you can go to our custom tutorial here: " + LINK
ADMIN = ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"] #Contains user IDs for those allowed to run $ commands

#initialize basic logging to see errors more easily
if LOGGER == True:
	logger = logging.getLogger('root')
	FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
	logging.basicConfig(format=FORMAT)
	logger.setLevel(logging.DEBUG)

#Global Variables, don't change these, these are just to make our lives easier when using the $log command
global LOG
LOG = False
global LOGC
LOGC = []
#pugbomb variable declared
global pbCooldown
pbCooldown = 100

#function that is called whenever there is an event, including status changes, join messages, typing status, emoji reactions, everything
def on_message(ws, message):
	#converts to usable string format
	s = message.encode('ascii')

	#converts to JSON so we can parse through it easier
	response = json.loads(s)
	print "PantherBot:LOG:message:" + response["type"]

	#Pugbomb cooldown incrementation
	global pbCooldown
	pbCooldown += 1

	#Checks if the event type returned by Slack is a message
	if "message" == response["type"]:
		global LOG, LOGC

		#If $log has been set to true it will save all spoken messages.
		if LOG == True and response["channel"] in LOGC:
			#sets file location to the logs folder and based on the day's date
			#this way if $log is enabled and the day rolls over, it will shift over to the new file without hiccup
			filename = "logs/" + response["channel"] + " " + str(datetime.date.today()) + ".txt"

			#API call for user info that posted the message, personnally this should be removed
			#its innefficient (and causes unnecessary API calls), we should make a locally stored list of users that have talked and reference that
			#and if they arent found, call this function and append that list
			temp_user = sc.api_call(
				"users.info",
				user = response["user"]
			)

			script_dir = os.path.dirname(__file__)
			fullDir = os.path.join(script_dir, filename)
			if os.path.isfile(fullDir) == True:
				target = open(fullDir, "a")
			else:
				target = open(fullDir, "w+")
			user_name = temp_user["user"]["profile"]["first_name"] + " " + temp_user["user"]["profile"]["last_name"]

			#format:
			#F_NAME L_NAME
			#[MESSAGE] [TIMESTAMP]
			target.write(user_name+ "\n")
			target.write(response["text"] + " [")
			target.write(response["ts"] + "]\n\n")
			target.close()

		#Riyan's denial
		if "U0LJJ7413" in response["user"]:
			if response["text"][:1] in ["!", "$"] or response["text"].lower() in ["hey pantherbot", "pantherbot ping"]:
				rMsg(response, "No.")
				return

		#Checks if message starts with an exclamation point, and does the respective task
		elif response["text"][:1] == "!":
			#put all ! command parameters into an array
			args = response["text"].split()
			#Command logic
			if args[0].lower() == "!catfact":
				rMsg(response, CatFacts.catFacts())
				return
			if args[0].lower() == "!coin":
				rMsg(response, Coin.coin())
				return
			if args[0].lower() == "!fortune":
				rMsg(response, GiveFortune.giveFortune())
				return
			if args[0].lower() == "!pugbomb":
				if pbCooldown > 99:
					m = Pugbomb.pugbomb(response)
					for s in m["pugs"]:
						rMsg(response, s)
					pbCooldown = 0
				else:
					rMsg(response, "Sorry, pugbomb is on cooldown")
				return
			if args[0].lower() == "!flip" or args[0].lower() == "!rage":
				rMsg(response, Flip.flip(args))
				return
			if args[0].lower() == "!unflip":
				rMsg(response, Unflip.unflip(args))
				return
			if args[0].lower() == "!taskme":
				taskArr = TaskMe.taskme()
				rMsg(response, "PantherBot challenges you to:\nIn the language of your choosing, " + taskArr[0])
				rMsg(response, "Sample Output:\n" + taskArr[1])
			if args[0].lower() == "!help":
				rMsg(response, Help.help())
				return
			if args[0].lower() == "!calendar":
				#Dont want to do an API call for something that isn't enabled
				if GOOGLECAL == True:
					#need to check allowed users but this can be set up properly later
					if response["user"] == "U3EAHHF40":
						rMsg(response, Calendar.determine(args, calendar))
					else:
						rMsg(response, "It seems you aren't authorized to add events to the calendar. If you believe this is a mistake, contact the person in charge of the Calendar, or the maintainer(s) of PantherBot")
				else:
					rMsg(response, "It seems Google Calendar is disabled, contact the PantherBot maintainer(s) if you believe this a mistake.")

		#Checks for a log command
		elif response["text"][:1] == "$":
			args = response["text"].split()
			#Command logic
			if args[0].lower() == "$log":
				if response["user"] in ADMIN:
					print "PantherBot:LOG:Approved User called $log"
					log(response, args)
					return
				else:
					rMsg(response, "It seems you aren't authorized to enable logging. If you believe this a mistake, contact the maintainer(s) of PantherBot")

		#If not an ! or $, checks if it should respond to another message format, like a greeting
		elif response["text"].lower() == "hey pantherbot":
			#returns user info that said hey
			temp_user = sc.api_call(
				"users.info",
				user = response["user"]
			)
			print "PantherBot:LOG:Greeting:We did it reddit"
			try:
				#attempts to send a message to Slack, this one is the only one that needs this try thing so far, no clue why
				rMsg(response, "Hello, " + temp_user["user"]["profile"]["first_name"] + "! :tada:")
			except:
				print "PantherBot:LOG:Greeting:Error in response"
		elif response["text"].lower() == "pantherbot ping":
			rMsg(response, "PONG")
	elif "team_join" == response["type"] and NEWUSERGREETING == True:
		print "Member joined team"
		print response
		sc.api_call(
			"chat.postMessage",
			channel=response["user"]["id"],
			text=GREETING,
			username=BOT_NAME,
			icon_url=BOT_ICON_URL
		)

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

#Unused things for WebSocketApp
def on_error(ws, error):
	print error

def on_close(ws):
	print "### closed ###"

#send a response message (sends to same channel as command was issued)
def rMsg(response, t):
	sc.api_call(
		"chat.postMessage",
		channel=response["channel"],
		text=t,
		username=BOT_NAME,
		icon_url=BOT_ICON_URL
	)
	print "PantherBot:LOG:Message sent"

#necessary shenanigans
if __name__ == "__main__":
	print "PantherBot:LOG:Beginning Execution... Setting up"

	#Checks if the system's encoding type is utf-8 and changes it to utf-8 if it isnt (its not on Windows by default)
	if sys.stdout.encoding != 'utf-8':
		sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
	if sys.stderr.encoding != 'utf-8':
		sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')

	#Toggleable, if you're not testing the Google Calendar API implementation or using this in a live environment that uses it, saves loading time and memory space.
	if GOOGLECAL == True:
		#Google API stuff
		#SOOOOO... Google doesnt like us using a newer version of oauth2, might have to downgrade when we put this on the Pi officially
		print "PantherBot:LOG:Starting Google API Authentication..."
		scopes = ['https://www.googleapis.com/auth/calendar']

		secret_location = os.path.dirname(__file__)
		secret_fullDir = os.path.join(secret_location, 'secrets', GOOGLECALSECRET)

		print "PantherBot:LOG:Searching for Google Credentials"
		credentials = ServiceAccountCredentials.from_json_keyfile_name(
		    secret_fullDir, scopes=scopes)

		print "PantherBot:LOG:Authenticating..."
		google_http_auth = credentials.authorize(Http())

		calendar = build('calendar', 'v3', http=google_http_auth)
		print "PantherBot:LOG:Authentication Successful. Should consider enabling debug to view OAuth message. Starting PantherBot"
		#print calendar.calendarList().list().execute()
	else:
		print "PantherBot:LOG:Google Calendar API not enabled, edit the `GOOGLECAL` variable to enable it. See Google Calendar Python API documentation about Google API Service Accounts on how to authenticate. Store your secret in the /secrets/ folder and edit the `GOOGLECALSECRET` variable with the file name"

	#If for some reason you need to debug without connecting to the Slack RTM API... this is for you.
	if SLACK == True:
		#Get Token from local system environment variables
		t = os.environ['SLACK_API_TOKEN']
		#initiates the SlackClient connection
		sc = SlackClient(t)

		#initiates connection to the server based on the token
		print "PantherBot:LOG:Starting RTM connection"
		bot_conn = sc.api_call(
			"rtm.start",
			token = t
		)

		#creates WebSocketApp based on the wss returned by the RTM API
		print "PantherBot:LOG:Starting WebSocketApplication and connection"
		ws = websocket.WebSocketApp(bot_conn["url"],
								on_message = on_message,
								on_error = on_error,
								on_close = on_close)

		#Keeps socket open
		ws.run_forever()
	else:
		print "PantherBot:LOG:Slack connection disabled... why?"
