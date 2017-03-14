# -*- coding: utf-8 -*-
"""
This module runs basically everything.

Attributes:
    VERSION = "1.1.8" (String): Version Number: release.version_num.revision_num

    # Config Variables
    BOT_NAME (String): Bot name that will appear in Slack on message posting
    BOT_ICON_URL (String): Bot icon that will appear in Slack on message posting
    SLACK (boolean): Config variable, toggles connecting to Slack RTM service
    GOOGLECAL (boolean): Config variable, toggles connecting to Google Calendar API service
    LOGGER (boolean): Config variable, toggles logger functionality
    GOOGLECALSECRET (String): Config variable, file name for google-calendar secret in the secrets/ folder
    NEWUSERGREETING (boolean): Config variable, toggles new user greeting for Slack team
    GREETING (String): Config variable, String to be sent to new users on team join
    EMOJI_LIST (List): List of Strings for emojis to be added to announcements
    USER_LIST (JSON): List of users in JSON format
    ADMIN (List): ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"] testing defaults
    ADMIN_COMMANDS (List): List of admin commands that cant be executed normallu
    TTPB (String): Config variable, sets channel for cleverbot integration
    GENERAL (Stirng): Config variable, sets channel for general name
    LOG (boolean): Global Variable
    LOGC (boolean): Global Variable
    pbCooldown (int): Global Variable

Todo:
    * Move otherMessage response to user USER_LIST instead of api call

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""


# Slack imports
from slackclient import SlackClient
# Google imports
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
# Other imports
import scripts
from scripts import commands
import os, io, sys, time, codecs, websocket, json, logging, random, logtofile  # noqa: 401
import re

# Version Number: release.version_num.revision_num
VERSION = "1.1.8"

# Config Variables
BOT_NAME = ""
BOT_ICON_URL = ""
SLACK = False
GOOGLECAL = False
LOGGER = False
GOOGLECALSECRET = ""
NEWUSERGREETING = False
GREETING = ""
EMOJI_LIST = ["party-parrot", "venezuela-parrot", "star2", "fiesta-parrot", "wasfi_dust", "dab"]  # noqa: 501
USER_LIST = []
ADMIN = []
ADMIN_COMMANDS = ["log", "calendar", "admin"]
TTPB = ""
GENERAL = ""

# Global variabls
global LOG
LOG = False
global LOGC
LOGC = []
global pbCooldown
pbCooldown = 100
polling_list = dict()


# function that is called whenever there is an event, including status changes, join messages, typing status, emoji reactions, everything  # noqa: 501
def on_message(ws, message):

    s = message.decode('utf-8')
    response = json.loads(unicode(s))
    print "PantherBot:LOG:message:" + response["type"]

    # Pugbomb cooldown incrementation
    global pbCooldown
    pbCooldown += 1
    global LOG
    global LOGC

    # Checks if the event type returned by Slack is a message
    if "message" == response["type"]:
        if "subtype" in response:
            if response["subtype"] == "bot_message":
                #polling logic
                if "POLL_BEGIN" in response["text"]:
                    polling_list[response["channel"]][0] = response["ts"]
                    temp_options = polling_list[response["channel"]][1]
                    for key in temp_options:
                        rreaction(response, temp_options[key].strip(":"))
                return
        # Checks LOG and LOGC values, then
        # If LOG has been set to true it will save all spoken messages.
        checkLog()
        if LOG and response["channel"] in LOGC:
            logtofile.log(sc, response)

        # Announcement reactions
        reactAnnouncement(response)
        # if riyansDenial(response):
        #     return
        if otherMessage(response):
            return
        if commandMessage(response):
            return
        if adminMessage(response):
            return

    elif "team_join" == response["type"]:
        if NEWUSERGREETING:
            newUserMessage(response)
        USER_LIST = sc.api_call(  # noqa: 841
            "users.list",
        )


def commandMessage(response):
    # Checks if message starts with an exclamation point, and does the respective task  # noqa: 501
    if response["text"][:1] == "!":
        global pbCooldown

        # put all ! command parameters into an array
        args = response["text"].split()
        com_text = args[0][1:].lower()
        args.pop(0)  # gets rid of the command


        # checks if command is an Admin command
        if com_text in ADMIN_COMMANDS:
            rmsg(response, ["Sorry, admin commands may only be used with the $ symbol (ie. `$admin`)"])  # noqa: 501
            return True


        # special cases for some functions
        if com_text == "pugbomb":
            if pbCooldown < 100:
                rmsg(response, ["Sorry, pugbomb is on cooldown"])
                return True
            else:
                pbCooldown = 0

        if com_text == "version":
            rmsg(response, [VERSION])
            return True

        if com_text == "talk":
            ch = channel_to_id([TTPB])
            c = ch[0]
            if response["channel"] != c:
                rmsg(response, ["Talk to me in #" + TTPB])
                return True

        if com_text[0] == '!':
            return True

        # list that contains the response and args for all methods
        method_args = []
        method_args.append(response)

        if com_text == "poll":
            method_args.append(polling_list[response["channel"]])
            method_args.append(sc)

        if len(args) > 0:
            method_args.append(args)
        # Attempts to find a command with the name matching the command given, and executes it  # noqa: 501
        try:
            called_function = getattr(commands[com_text], com_text)
            rmsg(response, called_function(*method_args))
            return True
        except:
            # If it fails, outputs that no command was found or syntax was broken.  # noqa: 501
            rmsg(response, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])  # noqa: 501
            return True
    return False


def adminMessage(response):
    # Repeats above except for admin commands
    if response["text"][:1] == "$":
        # Checks if message is longer than "$"
        if len(response["text"]) > 1:
            args = response["text"].split()
            com_text = args[0][1:].lower()
            args.pop(0)
            # Checks if pattern differs from admin commands
            # by containing digits or another "$" character
            com_pattern = (re.compile("[0-9]"), re.compile("[$]"))
            try:
                if com_pattern[0].search(com_text) or com_pattern[1].search(com_text):
                    return False
            except:
                pass

            if response["user"] in ADMIN:
                # Special case for calendar requiring unique arguments
                if com_text == "calendar":
                    if GOOGLECAL:
                        rmsg(response, scripts.calendar.calendar(args, calendar_obj))  # noqa: 501
                        return True
                l = []
                l.append(response)
                l.append(args)
                l.append(sc)
                l.append(rmsg)
                try:
                    f = getattr(commands[com_text], com_text)
                    f(*l)
                    return True
                except:
                    rmsg(response, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])  # noqa: 501
                    return True

            # Checks if command is an admin command
            elif com_text in ADMIN_COMMANDS:
                rmsg(response, ["It seems you aren't authorized to use admin commands. If you believe this a mistake, contact the maintainer(s) of PantherBot"])  # noqa: 501
                return True

    return False


def otherMessage(response):
    # If not an ! or $, checks if it should respond to another message format, like a greeting  # noqa: 501
    try:
        if re.match(".*panther +hackers.*", str(response["text"].lower())):
            rmsg(response, ["NO THIS IS PANTHERHACKERS"])
            return True
        elif response["text"].lower() == "hey pantherbot":
            # returns user info that said hey
            # TODO make this use USER_LIST
            temp_user = sc.api_call(
                "users.info",
                user = response["user"]  # noqa
            )
            print "PantherBot:LOG:Greeting:We did it reddit"
            rmsg(response, ["Hello, " + temp_user["user"]["profile"]["first_name"] + "! :tada:"])  # noqa: 501
            return True
        elif response["text"].lower() == "pantherbot ping":
            rmsg(response, ["PONG"])
            return True
        elif response["text"].lower() == ":rip: pantherbot" or response["text"].lower() == "rip pantherbot":  # noqa: 501
            rmsg(response, [":rip:"])
            return True
        elif re.match(".*panther +hackers.*", str(response["text"].lower())):
            rmsg(response, ["NO THIS IS PANTHERHACKERS"])
            return True
        elif "subtype" in response:
            if response["subtype"] == "channel_leave" or response["subtype"] == "group_leave":  # noqa: 501
                rmsg(response, ["Press F to pay respects"])
                return True
        return False
    except:
        print "Error with checking in otherMessage: likely the message contained unicode characters"


def riyansDenial(response):
    if "U0LJJ7413" in response["user"]:
        if response["text"][:1] in ["!", "$"] or response["text"].lower() in ["hey pantherbot", "pantherbot ping"]:  # noqa: 501
            rmsg(response, ["No."])
            return True
    return False


def newUserMessage(response):
    print "PantherBot:LOG:Member joined team"
    sc.api_call(
        "chat.postMessage",
        channel=response["user"]["id"],
        text=GREETING,
        username=BOT_NAME,
        icon_url=BOT_ICON_URL
    )


def reactAnnouncement(response):
    if GENERAL != "" and response["channel"] == GENERAL:
        temp_list = list(EMOJI_LIST)
        rreaction(response, "pantherbot")
        for x in range(0, 3):
            num = random.randrange(0, len(temp_list))
            rreaction(response, temp_list.pop(num))


# Less used WebSocket functions
def on_error(ws, error):
    print "PantherBot:LOG:ERROR"
    print error


def on_close(ws):
    print "PantherBot:LOG:Connection lost or closed..."


# send a response message (sends to same channel as command was issued)
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


def checkLog():
    global LOG
    global LOGC
    filename = "config/log.txt"
    script_dir = os.path.dirname(__file__)
    fullDir = os.path.join(script_dir, filename)
    if os.path.isfile(fullDir) == False:  # noqa
        target = open(fullDir, "w+")
        target.write(u'False')
        target.close()
    else:
        target = open(fullDir, "r")
    if target.readline().strip('\n') == "True":
        LOG = True
    else:
        LOG = False
    LOGC = [line.rstrip('\n') for line in target]
    target.close()


# necessary shenanigans
if __name__ == "__main__":
    print "PantherBot:LOG:Beginning Execution... Setting up"

    # Checks if the system's encoding type is utf-8 and changes it to utf-8 if it isnt (its not on Windows by default)  # noqa: 501
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')

    # load config files
    print "PantherBot:LOG:Loading config files"
    filename = "config/admin.txt"
    script_dir = os.path.dirname(__file__)
    fullDir = os.path.join(script_dir, filename)
    if not os.path.isfile(fullDir):
        target = io.open(fullDir, "w+", encoding='utf-8')
        target.close()
    ADMIN = [line.rstrip('\n') for line in open(fullDir)]

    filename = "config/bot.txt"
    script_dir = os.path.dirname(__file__)
    fullDir = os.path.join(script_dir, filename)
    if not os.path.isfile(fullDir):
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
    if not os.path.isfile(fullDir):
        target = open(fullDir, "w+")
        target.write('True\n')
        target.write('False\n')
        target.write('True\n')
        target.write('google-secret.json\n')
        target.write('True\n')
        target.write('Welcome to the team! You can get more help with Slack here: https://get.slack.help/\n')  # noqa: 501
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

    # initialize basic logging to see errors more easily
    if LOGGER:
        logger = logging.getLogger('root')
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=FORMAT)
        logger.setLevel(logging.DEBUG)

    # Toggleable, if you're not testing the Google Calendar API implementation or using this in a live environment that uses it, saves loading time and memory space.  # noqa: 501
    if GOOGLECAL:
        # Google API stuff
        # SOOOOO... Google doesnt like us using a newer version of oauth2, might have to downgrade when we put this on the Pi officially  # noqa: 501
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
        print "PantherBot:LOG:Authentication Successful. Should consider enabling debug to view OAuth message. Starting PantherBot"  # noqa: 501
        # print calendar.calendarList().list().execute()
    else:
        print "PantherBot:LOG:Google Calendar API not enabled, edit the `GOOGLECAL` variable to enable it. See Google Calendar Python API documentation about Google API Service Accounts on how to authenticate. Store your secret in the /secrets/ folder and edit the `GOOGLECALSECRET` variable with the file name"  # noqa: 501

    # If for some reason you need to debug without connecting to the Slack RTM API... this is for you.  # noqa: 501
    if SLACK:
        while True:
            try:
                t = ""
                # Get Token from secrets folder
                try:
                    filename = "secrets/slack_secret.txt"
                    script_dir = os.path.dirname(__file__)
                    fullDir = os.path.join(script_dir, filename)
                    target = io.open(fullDir, "r")
                    t = target.readline().rstrip("\n")
                except:
                    print "PantherBot:LOG:Cannot find Slack token"
                # initiates the SlackClient connection and Cleverbot API
                sc = SlackClient(t)

                # initiates connection to the server based on the token
                print "PantherBot:LOG:Starting RTM connection"
                bot_conn = sc.api_call(
                    "rtm.start",
                    token = t   # noqa:
                )

                # Update current USER_LIST (since members may join while PantherBot is off, I think its safe to make an API call every initial run)  # noqa: 501
                USER_LIST = sc.api_call(
                    "users.list"
                )

                polling_list = {}
                pub_channels = sc.api_call(
                    "channels.list",
                    exclude_archived=1
                )
                pri_channels = sc.api_call(
                    "groups.list",
                    exclude_archived=1
                )
                for c in pub_channels["channels"]:
                    polling_list[c["id"]] = ["",[],"none"]
                for c in pri_channels["groups"]:
                    polling_list[c["id"]] = ["",[],"none"]

                # Update current General Channel (usually announcements)
                li = channel_to_id(["announcements"])
                if not li:
                    li = channel_to_id(["general"])
                try:
                    GENERAL = li[0]
                except:
                    pass

                # creates WebSocketApp based on the wss returned by the RTM API
                print "PantherBot:LOG:Starting WebSocketApplication and connection"  # noqa: 501
                ws = websocket.WebSocketApp(bot_conn["url"],
                                        on_message=on_message,  # noqa
                                        on_error=on_error,  # noqa
                                        on_close=on_close)  # noqa:

                ws.run_forever(ping_interval=30, ping_timeout=10)
                time.sleep(10)
                print "PantherBot:LOG:Attempting to reconnect"
            except:
                print "PantherBot:LOG:Attempting to reconnect"
                time.sleep(10)
    else:
        print "PantherBot:LOG:Slack connection disabled... why?"
