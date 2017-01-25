#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Slack imports
from slackclient import SlackClient
#Google imports
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
#Other imports
import scripts
from scripts import commands
import os, pdb, io, sys, time, platform, subprocess, codecs, websocket, datetime, json, logging, random, logtofile

#Version Number: release.version_num.revision_num
VERSION = "1.1.6"

#Config Variables
BOT_NAME = "" #Set to whatever you would like the Bot to post his name as in Slack
BOT_ICON_URL = "" #Set to change whatever the profile picture is when the Bot posts a message
SLACK = False #Set to False to disable connecting to the Slack RTM API... for whatever reason
GOOGLECAL = False #Set to False to disable connecting and enabling the Google Calendar API integration
LOGGER = False #Set to True to get "detailed" error messages in the console. These error messages can vary from very helpful to utterly useless
GOOGLECALSECRET = "" #Can make this a system environment variable if you really want to be careful
NEWUSERGREETING = False #Set to True to send users that join the Slack Team a message (GREETING), appended with a link (LINK) (used for whatever you want, in our case, a "How to Use Slack" document)
GREETING = "" #Set to a custom greeting loaded from config/settings.txt
EMOJI_LIST = ["party-parrot", "venezuela-parrot", "star2", "fiesta-parrot", "wasfi_dust", "dab"]
USER_LIST = [] #User list loaded at startup and on user join that contains list of team members.
ADMIN = [] #testing defaults: ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"] Contains user IDs for those allowed to run $ commands. loaded from config/admin.txt
ADMIN_COMMANDS = ["log", "calendar", "admin"]
TTPB = ""
GENERAL = ""
LOG = False
LOGC = []
#Global variabls
#pugbomb variable declared
global pbCooldown
pbCooldown = 100

#function that is called whenever there is an event, including status changes, join messages, typing status, emoji reactions, everything
def on_message(ws, message):
	s = message
	response = json.loads(s)
	print "PantherBot:LOG:message:" + response["type"]

	#Pugbomb cooldown incrementation
	global pbCooldown
	pbCooldown += 1

	#Checks if the event type returned by Slack is a message
	if "message" == response["type"]:
		if "subtype" in response:
			if response["subtype"] == "bot_message":
				return

		#Check LOG and LOGC
		LOG = False
		LOGC = []
		filename = "config/log.txt"
		script_dir = os.path.dirname(__file__)
		fullDir = os.path.join(script_dir, filename)
		if os.path.isfile(fullDir) == False:
			target = open(fullDir, "w+")
			target.write(u'False')
			target.close()
		else:
			target = open(fullDir, "r")
		if target.readline().strip('\n') == "True":
			LOG = True
		LOGC = [line.rstrip('\n') for line in target]
		target.close()

		#If $log has been set to true it will save all spoken messages.
		if LOG == True and response["channel"] in LOGC:
			logtofile.log(sc, response)

		#Announcement reactions
		if GENERAL != "" and response["channel"] == GENERAL:
			temp_list = list(EMOJI_LIST)
			print temp_list
			rreaction(response, "pantherbot")
			for x in  range(0, 3):
				num = random.randrange(0,len(temp_list))
				rreaction(response, temp_list.pop(num))

		#Riyan's denial
		#if "U0LJJ7413" in response["user"]:
		#	if response["text"][:1] in ["!", "$"] or response["text"].lower() in ["hey pantherbot", "pantherbot ping"]:
		#		rmsg(response, "No.")
		#		return

		#Checks if message starts with an exclamation point, and does the respective task
		if response["text"][:1] == "!":
			#put all ! command parameters into an array
			args = response["text"].split()
			com_text = args[0][1:].lower()
			args.pop(0) #gets rid of the command
			#checks if command is an Admin command
			if com_text in ADMIN_COMMANDS:
				rmsg(response, ["Sorry, admin commands may only be used with the $ symbol (ie. `$admin`)"])
				return
			#special cases for some functions
			if com_text == "pugbomb":
				if pbCooldown < 100:
					rmsg(response, ["Sorry, pugbomb is on cooldown"])
					return
				else:
					pbCooldown = 0
			if com_text == "version":
				rmsg(response, [VERSION])
				return
			if com_text == "talk":
				ch = channel_to_id([TTPB])
				c = ch[0]
				if response["channel"] != c:
					rmsg(response, ["Talk to me in #" + TTPB])
					return


			#list that contains the response and args for all methods
			l = []
			l.append(response)
			if len(args) > 0:
				l.append(args)
			#Attempts to find a command with the name matching the command given, and executes it
			try:
				f = getattr(commands[com_text], com_text)
				rmsg(response, f(*l))
			except:
				#If it fails, outputs that no command was found or syntax was broken.
				rmsg(response, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])

		#Repeats above except for admin commands
		elif response["text"][:1] == "$":
			if response["user"] in ADMIN:
				args = response["text"].split()
				com_text = args[0][1:].lower()
				args.pop(0)
				#Special case for calendar requiring unique arguments
				if com_text == "calendar":
					if GOOGLECAL:
						rmsg(response, scripts.calendar.calendar(args, calendar_obj))
						return
				l = []
				l.append(response)
				l.append(args)
				l.append(sc)
				l.append(rmsg)
				try:
					f = getattr(commands[com_text], com_text)
					f(*l)
				except:
					rmsg(response, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])
			else:
				rmsg(response, "It seems you aren't authorized to use admin commands. If you believe this a mistake, contact the maintainer(s) of PantherBot")

		#If not an ! or $, checks if it should respond to another message format, like a greeting
		elif response["text"].lower() == "hey pantherbot":
			#returns user info that said hey
			#TODO make this use USER_LIST
			temp_user = sc.api_call(
				"users.info",
				user = response["user"]
			)
			print "PantherBot:LOG:Greeting:We did it reddit"
			try:
				#attempts to send a message to Slack, this one is the only one that needs this try thing so far, no clue why
				rmsg(response, ["Hello, " + temp_user["user"]["profile"]["first_name"] + "! :tada:"])
			except:
				print "PantherBot:LOG:Greeting:Error in response"

		elif response["text"].lower() == "pantherbot ping":
			rmsg(response, ["PONG"])

		elif response["text"].lower() == ":rip: pantherbot" or response["text"].lower() == "rip pantherbot":
			rmsg(response, [":rip:"])
		elif "panther hackers" in str(response["text"].lower()):
			rmsg(response, ["NO THIS IS PANTHERHACKERS"])
		elif "subtype" in response:
			if response["subtype"] == "channel_leave":
				rmsg(response, ["Press F to pay respects"])

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
		USER_LIST = sc.api_call(
			"users.list",
		)

#Less used WebSocket functions
def on_error(ws, error):
	print "PantherBot:LOG:ERROR"
	print error

def on_close(ws):
	print "PantherBot:LOG:Connection lost or closed..."

#send a response message (sends to same channel as command was issued)
def rmsg(response, l):
	for text in l:
		sc.api_call(
			"chat.postMessage",
			channel=response["channel"],
			text=text,
			username=BOT_NAME,
			icon_url=BOT_ICON_URL
		)
		print "PantherBot:LOG:Message sent"

def rreaction(response, emoji):
	sc.api_call(
		"reactions.add",
		name=emoji,
		channel=response["channel"],
		timestamp=response["ts"]
	)
	print "PantherBot:LOG:Reaction posted"

def channel_to_id(channel_names):
	pub_channels = sc.api_call(
		"channels.list",
		exclude_archived=1
	)
	pri_channels = sc.api_call(
		"groups.list",
		exclude_archived=1
	)
	li = []
	for channel in pub_channels["channels"]:
		for num in range(0, len(channel_names)):
			if channel["name"].lower() == channel_names[num].lower():
				li.append(channel["id"])
	# Same as above
	for channel in pri_channels["groups"]:
		for num in range(0, len(channel_names)):
			if channel["name"].lower() == channel_names[num].lower():
				li.append(channel["id"])
	return li

#necessary shenanigans
if __name__ == "__main__":
	print "PantherBot:LOG:Beginning Execution... Setting up"

	#Checks if the system's encoding type is utf-8 and changes it to utf-8 if it isnt (its not on Windows by default)
	if sys.stdout.encoding != 'utf-8':
		sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
	if sys.stderr.encoding != 'utf-8':
		sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')

	#Used to load config files and stuff.
	#not implemented yet
	#load config files
	print "PantherBot:LOG:Loading config files"
	filename = "config/admin.txt"
	script_dir = os.path.dirname(__file__)
	fullDir = os.path.join(script_dir, filename)
	if os.path.isfile(fullDir) == False:
		target = io.open(fullDir, "w+", encoding='utf-8')
		target.close()
	ADMIN = [line.rstrip('\n') for line in open(fullDir)]

	filename = "config/bot.txt"
	script_dir = os.path.dirname(__file__)
	fullDir = os.path.join(script_dir, filename)
	if os.path.isfile(fullDir) == False:
		target = open(fullDir, "w+")
		target.write('PantherBot\n')
		target.write('http://i.imgur.com/QKaLCX7.png\n')
		target.close()
	target = io.open(fullDir, "r")
	BOT_NAME = target.readline().rstrip('\n')
	BOT_ICON_URL = target.readline().rstrip('\n')
	target.close()

	filename = "config/settings.txt"
	script_dir = os.path.dirname(__file__)
	fullDir = os.path.join(script_dir, filename)
	if os.path.isfile(fullDir) == False:
		target = open(fullDir, "w+")
		target.write('True\n')
		target.write('False\n')
		target.write('False\n')
		target.write('google-secret.json\n')
		target.write('True\n')
		target.write('Welcome to the team! You can get more help with Slack here: https://get.slack.help/\n')
		target.write('talk-to-pantherbot')
		target.close()
	target = io.open(fullDir, "r")
	if target.readline().rstrip('\n') == "True":
		SLACK = True
	if target.readline().rstrip('\n') == "True":
		GOOGLECAL = True
	if target.readline().rstrip('\n') == "True":
		LOGGER = True
	GOOGLECALSECRET = target.readline().rstrip('\n')
	if target.readline().rstrip('\n') == "True":
		GREETING = True
	NEWUSERGREETING = target.readline().rstrip('\n')
	TTPB = target.readline().rstrip('\n')
	target.close()

	#initialize basic logging to see errors more easily
	if LOGGER == True:
		logger = logging.getLogger('root')
		FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
		logging.basicConfig(format=FORMAT)
		logger.setLevel(logging.DEBUG)

	#Toggleable, if you're not testing the Google Calendar API implementation or using this in a live environment that uses it, saves loading time and memory space.
	if GOOGLECAL == True:
		#Google API stuff
		#SOOOOO... Google doesnt like us using a newer version of oauth2, might have to downgrade when we put this on the Pi officially
		print "PantherBot:LOG:Starting Google API Authentication..."
		scopes = ['https://www.googleapis.com/auth/calendar']

		secret_location = os.path.dirname(__file__)
		secret_fullDir = os.path.join(secret_location, 'secrets')
		secret_fullDir = os.path.join(secret_fullDir, GOOGLECALSECRET)

		print "PantherBot:LOG:Searching for Google Credentials"
		credentials = ServiceAccountCredentials.from_json_keyfile_name(
			secret_fullDir, scopes=scopes)

		print "PantherBot:LOG:Authenticating..."
		google_http_auth = credentials.authorize(Http())

		calendar_obj = build('calendar', 'v3', http=google_http_auth)
		print "PantherBot:LOG:Authentication Successful. Should consider enabling debug to view OAuth message. Starting PantherBot"
		#print calendar.calendarList().list().execute()
	else:
		print "PantherBot:LOG:Google Calendar API not enabled, edit the `GOOGLECAL` variable to enable it. See Google Calendar Python API documentation about Google API Service Accounts on how to authenticate. Store your secret in the /secrets/ folder and edit the `GOOGLECALSECRET` variable with the file name"

	#If for some reason you need to debug without connecting to the Slack RTM API... this is for you.
	if SLACK == True:
		while True:
			try:
				t = ""
				#Get Token from secrets folder
				try:
					filename = "secrets/slack_secret.txt"
					script_dir = os.path.dirname(__file__)
					fullDir = os.path.join(script_dir, filename)
					target = io.open(fullDir, "r")
					t = target.readline().rstrip("\n")
				except:
					print "PantherBot:LOG:Cannot find Slack token"
				#initiates the SlackClient connection
				sc = SlackClient(t)

				#initiates connection to the server based on the token
				print "PantherBot:LOG:Starting RTM connection"
				bot_conn = sc.api_call(
					"rtm.start",
					token = t
				)

				#Update current USER_LIST (since members may join while PantherBot is off, I think its safe to make an API call every initial run)
				USER_LIST = sc.api_call(
					"users.list"
				)

				#Update current General Channel (usually announcements)
				li = channel_to_id(["announcements"])
				if not li:
					li = channel_to_id(["general"])
				try:
					GENERAL = li[0]
				except:
					pass

				#Initiates CleverBot item that will be passed to !talk function
				#cb = Cleverbot('PantherBot')

				#creates WebSocketApp based on the wss returned by the RTM API
				print "PantherBot:LOG:Starting WebSocketApplication and connection"
				ws = websocket.WebSocketApp(bot_conn["url"],
										on_message = on_message,
										on_error = on_error,
										on_close = on_close)

				ws.run_forever(ping_interval=30, ping_timeout=10)
				time.sleep(10)
				print "PantherBot:LOG:Attempting to reconnect"
			except:
				print "PantherBot:LOG:Attempting to reconnect"
				time.sleep(10)
	else:
		print "PantherBot:LOG:Slack connection disabled... why?"
