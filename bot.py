# -*- coding: utf-8 -*-
"""
This module runs basically everything.

Attributes:
    VERSION = "2.0.0" (String): Version Number: release.version_num.revision_num

    # Config Variables
    EMOJI_LIST (List): List of Strings for emojis to be added to announcements
    USER_LIST (JSON): List of users in JSON format
    ADMIN (List): ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"] testing defaults
    ADMIN_COMMANDS (List): List of admin commands that cant be executed normally
    TTPB (String): Config variable, sets channel for cleverbot integration
    GENERAL (Stirng): Config variable, sets channel for general's name
    LOG (boolean): Global Variable
    LOGC (boolean): Global Variable
    pbCooldown (int): Global Variable

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from slackclient import SlackClient
import threading, websocket, json, re, time, codecs, random, logtofile
import scripts
from scripts import commands

class Bot:
    ADMIN = ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"]
    ADMIN_COMMANDS = ["log", "calendar", "admin"]
    EMOJI_LIST = ["party-parrot", "venezuela-parrot", "star2", "fiesta-parrot", "wasfi_dust", "dab"]
    GENERAL_CHANNEL = ""
    TTPB = "talk-to-pantherbot"
    GOOGLECAL = False
    VERSION = "2.0.0"

    def __init__(self, token, is_websocket=True, bot_name=""):
        self.SC = None
        self.BOT_NAME = bot_name
        self.BOT_ICON_URL = "http://i.imgur.com/QKaLCX7.png"
        self.USER_LIST = None
        self.POLLING_LIST = dict()
        self.WEBSOCKET = None
        self.THREADS = []
        self.pb_cooldown = True
        self.connect_to_slack(token, is_websocket)

    def on_message(self, ws, message):
        message_thread = threading.Thread(target=self.on_message_thread, args=(message,))
        self.THREADS.append(message_thread)
        message_thread.start()
        return

    def on_message_thread(self, message):
        s = message.decode('utf-8')
        response = json.loads(unicode(s))
        print "PantherBot:LOG:message:" + response["type"]
        
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

            # Announcement reactions
            self.react_announcement(response)
            # if riyansDenial(response):
            #     return
            if self.other_message(response):
                return
            if self.command_message(response):
                return
            if self.admin_message(response):
                return

    def on_error(self, ws, error):
        return

    def on_close(self, ws):
        return

    def on_open(self, ws):
        self.smsg("pantherbot-dev", "Bot successfully started")

    def connect_to_slack(self, token, is_websocket):
        self.SC = SlackClient(token)

        if is_websocket:
            # Initiates connection to the server based on the token, receives websocket URL "bot_conn"
            print "PantherBot:LOG:Starting RTM connection"
            bot_conn = self.SC.api_call(
                "rtm.start",
                token = token
            )

            print "PantherBot:LOG:Initializing info"
            self.initialize_info()

            # Creates WebSocketApp based on the URL returned by the RTM API
            # Assigns local methods to websocket methods
            print "PantherBot:LOG:Initializing WebSocketApplication"  # noqa: 501
            self.WEBSOCKET = websocket.WebSocketApp(bot_conn["url"],
                                    on_message=self.on_message,  # noqa
                                    on_error=self.on_error,  # noqa
                                    on_close=self.on_close,
                                    on_open=self.on_open)  # noqa:

    def initialize_info(self):
        # Update current USER_LIST (since members may join while PantherBot is off, its safe to make an API call every initial run)  # noqa: 501
        # When database is implemented, this should be sure to cross reference the database's list with this so new users are added.
        self.USER_LIST = self.SC.api_call(
            "users.list"
        )

        # List of polls for all channels
        self.POLLING_LIST = {}
        pub_channels = self.SC.api_call(
            "channels.list",
            exclude_archived=1
        )
        pri_channels = self.SC.api_call(
            "groups.list",
            exclude_archived=1
        )
        for c in pub_channels["channels"]:
            # Sets channel polling option to an array of format ["", [], "none"]
            self.POLLING_LIST[c["id"]] = ["",[],"none"]
        for c in pri_channels["groups"]:
            self.POLLING_LIST[c["id"]] = ["",[],"none"]

        # Update current General Channel (usually announcements)
        li = self.channels_to_ids(["announcements"])
        if not li:
            li = self.channels_to_ids(["general"])
        try:
            if Bot.GENERAL_CHANNEL is "":
                Bot.GENERAL_CHANNEL = li[0]
        except:
            pass

    # Returns a list of channel IDs searched for by name
    def channels_to_ids(self, channel_names):
        pub_channels = self.SC.api_call(
            "channels.list",
            exclude_archived=1
        )
        pri_channels = self.SC.api_call(
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

    # Response Message
    # Sends a message to the same channel that response originates from
    def rmsg(self, response, l):
        for text in l:
            self.SC.api_call(
                "chat.postMessage",
                channel=response["channel"],
                text=text,
                username=self.BOT_NAME,
                icon_url=self.BOT_ICON_URL
            )
            print "PantherBot:LOG:Message sent"

    # Send Message
    # Sends a message to the specified channel (looks up by channel name, unless is_id is True)
    def smsg(self, channel, text, is_id=False):
        if not is_id:
            channel_id = self.channels_to_ids([channel])[0]
        else:
            channel_id = channel
        self.SC.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=text,
            username=self.BOT_NAME,
            icon_url=self.BOT_ICON_URL
        )
        print "PantherBot:LOG:Message sent"

    # Command Messages are messages that begin with the `!` prefix
    # Returns True if a response or trigger was used in this method
    def command_message(self, response):
        # Checks if message starts with an exclamation point, and does the respective task 
        if response["text"][:1] == "!":
            # Put all ! command parameters into an array
            args = response["text"].split()
            com_text = args[0][1:].lower()
            args.pop(0)  # gets rid of the command

            # Checks if command is an Admin command
            if com_text in self.ADMIN_COMMANDS:
                self.rmsg(response, ["Sorry, admin commands may only be used with the $ symbol (ie. `$admin`)"]) 
                return True

            # Special cases for some functions
            if com_text == "pugbomb":
                if not self.pb_cooldown:
                    self.rmsg(response, ["Sorry, pugbomb is on cooldown"])
                    return True
                else:
                    self.pb_cooldown = False

            if com_text == "version":
                self.rmsg(response, [self.VERSION])
                return True

            if com_text == "talk":
                ch = self.channels_to_ids([TTPB])
                c = ch[0]
                if response["channel"] != c:
                    self.rmsg(response, ["Talk to me in #" + TTPB])
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
            # Attempts to find a command with the name matching the command given, and executes it
            try:
                called_function = getattr(commands[com_text], com_text)
                self.rmsg(response, called_function(*method_args))
                return True
            except:
                # If it fails, outputs that no command was found or syntax was broken.
                self.rmsg(response, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])
                return True
        return False

    # Admin Messages are messages that begin with the `$` prefix
    # Returns True if a response or trigger was used in this method
    def admin_message(self, response):
        # Repeats above except for admin commands
        if response["text"][:1] == "$":
            # Checks if message is longer than "$"
            if len(response["text"]) > 1:
                args = response["text"].split()
                com_text = args[0][1:].lower()
                args.pop(0)
                # Checks if pattern differs from admin commands
                # by containing digits or another "$" character
                if any(i.isdigit() for i in com_text) or ('$' in com_text):
                    return False

                if response["user"] in self.ADMIN:
                    # Special case for calendar requiring unique arguments
                    if com_text == "calendar":
                        if GOOGLECAL:
                            self.rmsg(response, scripts.calendar.calendar(args, calendar_obj))  # noqa: 501
                            return True
                    l = []
                    l.append(response)
                    l.append(args)
                    l.append(self.SC)
                    l.append(self.rmsg)
                    try:
                        f = getattr(commands[com_text], com_text)
                        f(*l)
                        return True
                    except:
                        self.rmsg(response, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])
                        return True

                # Checks if command is an admin command
                elif com_text in self.ADMIN_COMMANDS:
                    self.rmsg(response, ["It seems you aren't authorized to use admin commands. If you believe this a mistake, contact the maintainer(s) of PantherBot"])
                    return True
                else:
                    self.rmsg(response, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])

        return False

    # Other Messages are messages that don't follow standard conventions (such as "Hey PantherBot!")
    # Returns True if a response or trigger was used in this method
    def other_message(self, response):
        # If not an ! or $, checks if it should respond to another message format, like a greeting 
        try:
            if re.match(".*panther +hackers.*", str(response["text"].lower())):
                self.rmsg(response, ["NO THIS IS PANTHERHACKERS"])
                return True
            elif response["text"].lower() == "hey pantherbot":
                # returns user info that said hey
                # TODO make this use USER_LIST
                temp_user = self.SC.api_call(
                    "users.info",
                    user = response["user"]  # noqa
                )
                print "PantherBot:LOG:Greeting:We did it reddit"
                self.rmsg(response, ["Hello, " + temp_user["user"]["profile"]["first_name"] + "! :tada:"])
                return True
            elif response["text"].lower() == "pantherbot ping":
                self.rmsg(response, ["PONG"])
                return True
            elif response["text"].lower() == ":rip: pantherbot" or response["text"].lower() == "rip pantherbot":
                self.rmsg(response, [":rip:"])
                return True
            elif re.match(".*panther +hackers.*", str(response["text"].lower())):
                self.rmsg(response, ["NO THIS IS PANTHERHACKERS"])
                return True
            elif "subtype" in response:
                if response["subtype"] == "channel_leave" or response["subtype"] == "group_leave": 
                    self.rmsg(response, ["Press F to pay respects"])
                    return True
            return False
        except:
            print "Error with checking in other_message: likely the message contained unicode characters"

    # Reacts to all messages posted in the GENERAL channel with a pre-defined list of emojis
    def react_announcement(self, response):
        if self.GENERAL_CHANNEL != "" and response["channel"] == self.GENERAL_CHANNEL:
            temp_list = list(self.EMOJI_LIST)
            self.rreaction(response, "pantherbot")
            for x in range(0, 3):
                num = random.randrange(0, len(temp_list))
                self.rreaction(response, temp_list.pop(num))

    def rreaction(self, response, emoji):
        self.SC.api_call(
            "reactions.add",
            name=emoji,
            channel=response["channel"],
            timestamp=response["ts"]
        )
        print "PantherBot:LOG:Reaction posted"

    def riyans_denial(self, response):
        if "U0LJJ7413" in response["user"]:
            if response["text"][:1] in ["!", "$"] or response["text"].lower() in ["hey pantherbot", "pantherbot ping"]: 
                self.rmsg(response, ["No."])
                return True
        return False