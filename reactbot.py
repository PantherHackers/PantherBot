# -*- coding: utf-8 -*-
"""
This module runs basically everything.

Attributes:
    VERSION = "2.0.0" (String): Version Number: release.version_num.revision_num

    # Config Variables
    EMOJI_LIST (List): List of Strings for emojis to be added to announcements
    USER_LIST (JSON): List of users in JSON format
    ADMIN (List): ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"] testing defaults
    TTPB (String): Config variable, sets channel for cleverbot integration
    GENERAL (Stirng): Config variable, sets channel for general's name
    LOG (boolean): Global Variable
    LOGC (boolean): Global Variable

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from slackclient import SlackClient
import threading, websocket, json, re, time, codecs, random
import scripts
from bot import Bot
from scripts import commands
from sqlalchemy import create_engine, MetaData, Column, Table, ForeignKey, Integer, String

class ReactBot(Bot):
    def __init__(self, token, bot_name=""):
        super(ReactBot, self).__init__(token, bot_name)
        self.connect_to_slack(token)
        self.setup_tables()

    def connect_to_slack(self, token):
        # Initiates connection to the server based on the token, receives websocket URL "bot_conn"
        print "PantherBot:LOG:Starting RTM connection"
        bot_conn = self.SLACK_CLIENT.api_call(
            "rtm.start",
            token = token
        )

        print "PantherBot:LOG:Initializing info"
        self.initialize_info()

        # Creates WebSocketApp based on the URL returned by the RTM API
        # Assigns local methods to websocket methods
        print "PantherBot:LOG:Initializing WebSocketApplication"
        self.WEBSOCKET = websocket.WebSocketApp(bot_conn["url"],
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close,
                                on_open=self.on_open)

    def initialize_info(self):
        # Update current USER_LIST (since members may join while PantherBot is off, its safe to make an API call every initial run)
        # When database is implemented, this should be sure to cross reference the database's list with this so new users are added.
        self.USER_LIST = self.SLACK_CLIENT.api_call(
            "users.list"
        )

        # List of polls for all channels
        self.POLLING_LIST = {}
        pub_channels = self.SLACK_CLIENT.api_call(
            "channels.list",
            exclude_archived=1
        )
        pri_channels = self.SLACK_CLIENT.api_call(
            "groups.list",
            exclude_archived=1
        )
        for c in pub_channels["channels"]:
            # Sets channel polling option to an array of format ["", [], "none"]
            self.POLLING_LIST[c["id"]] = ["",[],"none"]
        for c in pri_channels["groups"]:
            self.POLLING_LIST[c["id"]] = ["",[],"none"]

        # Update current General Channel (usually announcements)
        temp_list_of_channels = Bot.channels_to_ids(self, ["announcements"])
        if not temp_list_of_channels:
            temp_list_of_channels = Bot.channels_to_ids(self, ["general"])
        try:
            if Bot.GENERAL_CHANNEL is "":
                Bot.GENERAL_CHANNEL = temp_list_of_channels[0]
        except:
            print "PantherBot:LOG:The #general channel has been renamed to a non-default value"

    def on_message(self, ws, message):
        message_thread = threading.Thread(target=self.on_message_thread, args=(message,))
        self.THREADS.append(message_thread)
        message_thread.start()
        return

    def on_message_thread(self, message):
        s = message.decode('utf-8')
        message_json = json.loads(unicode(s))
        print "PantherBot:LOG:message:" + message_json["type"]
        
        #Logging event before execution
        self.log_event(message_json)
        
        if "message" == message_json["type"]:
            if "subtype" in message_json:
                if message_json["subtype"] == "bot_message":
                    #polling logic
                    if "POLL_BEGIN" in message_json["text"]:
                        self.POLLING_LIST[message_json["channel"]][0] = message_json["ts"]
                        temp_options = self.POLLING_LIST[message_json["channel"]][1]
                        for key in temp_options:
                            Bot.emoji_reaction(self, message_json, temp_options[key].strip(":"))
                    return

            # Announcement reactions
            self.react_announcement(message_json)

            # General commands
            # if riyansDenial(message_json):
            #     return
            if self.other_message(message_json):
                return
            if self.command_message(message_json):
                return
            if self.admin_message(message_json):
                return

    def on_error(self, ws, error):
        return

    def on_close(self, ws):
        return

    def on_open(self, ws):
        Bot.send_msg(self, "pantherbot-dev", "Bot successfully started")

    # message_json Message
    # Sends a message to the same channel that message_json originates from
    def response_message(self, message_json, l):
        for text in l:
            self.SLACK_CLIENT.api_call(
                "chat.postMessage",
                channel=message_json["channel"],
                text=text,
                username=self.BOT_NAME,
                icon_url=self.BOT_ICON_URL
            )
            print "PantherBot:LOG:Message sent"

    # Command Messages are messages that begin with the `!` prefix
    # Returns True if a message_json or trigger was used in this method
    def command_message(self, message_json):
        # Checks if message starts with an exclamation point, and does the respective task 
        if message_json["text"][:1] == "!":
            # Checks if the message is longer than a single character
            if len(message_json["text"]) <= 1:
                return False

            # Put all ! command parameters into an array
            args = message_json["text"].split()
            com_text = args[0][1:].lower()
            args.pop(0)  # gets rid of the command

            # Checks if pattern differs from command messages
            # by containing digits or another "$" character
            if any(i.isdigit() for i in com_text) or ('!' in com_text):
                return False

            if com_text == "version":
                self.response_message(message_json, [self.VERSION])
                return True

            if com_text == "talk":
                ch = Bot.channels_to_ids(self, [TTPB])
                c = ch[0]
                if message_json["channel"] != c:
                    self.response_message(message_json, ["Talk to me in #" + TTPB])
                    return True

            # list that contains the message_json and args for all methods
            method_args = []
            method_args.append(message_json)

            if com_text == "poll":
                method_args.append(self.polling_list[message_json["channel"]])
                method_args.append(self.SLACK_CLIENT)

            if com_text == "pugbomb":
                method_args.append(self.pb_cooldown)

            if len(args) > 0:
                method_args.append(args)
            
            # This is in a try statement since it is checking if a module exists with the com_text name,
            # It makes the try statement that was previously around the `called_function` section below much smaller,
            # and also less likely to skip an error that should be printed to the console.
            try:
                # Check if the command is an admin command using the script's self-declaration method
                check_admin_function = getattr(commands[com_text], "is_admin_command")
                if check_admin_function():
                    self.response_message(message_json, ["Sorry, admin commands may only be used with the $ symbol (ie. `$admin`)"])
                    return True
            except:
                # If it fails, outputs that no command was found or syntax was broken, since all scripts must follow this convention.
                self.response_message(message_json, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])
                return True

            # Finds the command with the name matching the text given, and executes it, assumed to exist because of above check
            called_function = getattr(commands[com_text], com_text)
            script_response = called_function(*method_args)
            if script_response.status_code is 0:
                self.response_message(message_json, script_response.messages_to_send)
            else:
                error_cleanup = getattr(script_response.module_called, "error_cleanup")
                script_response = error_cleanup(script_response.status_code)
                self.response_message(message_json, script_response.messages_to_send)
            if script_response.special_condition:
                special_condition_function = getattr(script_response.module_called, "special_condition")
                special_condition_function(self)
            return True

        return False

    # Admin Messages are messages that begin with the `$` prefix
    # Returns True if a message_json or trigger was used in this method
    def admin_message(self, message_json):
        # Repeats above except for admin commands
        if message_json["text"][:1] == "$":
            # Checks if message is longer than "$"
            if len(message_json["text"]) > 1:
                args = message_json["text"].split()
                com_text = args[0][1:].lower()
                args.pop(0)
                
                # Checks if pattern differs from admin commands
                # by containing digits or another "$" character
                if any(i.isdigit() for i in com_text) or ('$' in com_text):
                    return False

                # list that contains the message_json and args for all methods
                method_args = []
                method_args.append(message_json)
                method_args.append(args)
                method_args.append(self.SLACK_CLIENT)
                method_args.append(self)
                method_args.append(self.response_message)
                
                # This is in a try statement since it is checking if a module exists with the com_text name,
                # It makes the try statement that was previously around the `called_function` section below much smaller,
                # and also less likely to skip an error that should be printed to the console.
                try:
                    # Check if the command is an admin command using the script's self-declaration method
                    check_admin_function = getattr(commands[com_text], "is_admin_command")
                    if not check_admin_function():
                        self.response_message(message_json, ["Sorry, normal commands should be used with the `!` prefix (ie `!coin`)"])
                        return True
                except:
                    # If it fails, outputs that no command was found or syntax was broken, since all scripts must follow this convention.
                    self.response_message(message_json, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])
                    return True

                if message_json["user"] not in self.ADMIN:
                    print message_json["user"]
                    print self.ADMIN
                    self.response_message(message_json, ["You don't seem to be an authorized user to use these commands."])
                    return True

                # Finds the command with the name matching the text given, and executes it, assumed to exist because of above check
                called_function = getattr(commands[com_text], com_text)
                script_response = called_function(*method_args)
                if script_response.status_code is 0:
                    self.response_message(message_json, script_response.messages_to_send)
                else:
                    error_cleanup = getattr(script_response.module_called, "error_cleanup")
                    script_response = error_cleanup(script_response.status_code)
                    self.response_message(message_json, script_response.messages_to_send)
                if script_response.special_condition:
                    special_condition_function = getattr(script_response.module_called, "special_condition")
                    special_condition_function(self)
                return True

        return False

    # Other Messages are messages that don't follow standard conventions (such as "Hey PantherBot!")
    # Returns True if a message_json or trigger was used in this method
    def other_message(self, message_json):
        # If not an ! or $, checks if it should respond to another message format, like a greeting 
        try:
            if re.match(".*panther +hackers.*", str(message_json["text"].lower())):
                self.response_message(message_json, ["NO THIS IS PANTHERHACKERS"])
                return True
            elif message_json["text"].lower() == "hey pantherbot":
                # returns user info that said hey
                # TODO make this use USER_LIST
                temp_user = self.SLACK_CLIENT.api_call(
                    "users.info",
                    user = message_json["user"]
                )
                print "PantherBot:LOG:Greeting:We did it reddit"
                self.response_message(message_json, ["Hello, " + temp_user["user"]["profile"]["first_name"] + "! :tada:"])
                return True
            elif message_json["text"].lower() == "pantherbot ping":
                self.response_message(message_json, ["PONG"])
                return True
            elif message_json["text"].lower() == ":rip: pantherbot" or message_json["text"].lower() == "rip pantherbot":
                self.response_message(message_json, [":rip:"])
                return True
            elif re.match(".*panther +hackers.*", str(message_json["text"].lower())):
                self.response_message(message_json, ["NO THIS IS PANTHERHACKERS"])
                return True
            elif "subtype" in message_json:
                if message_json["subtype"] == "channel_leave" or message_json["subtype"] == "group_leave": 
                    self.response_message(message_json, ["Press F to pay respects"])
                    return True
            return False
        except:
            print "Error with checking in other_message: likely the message contained unicode characters"

    # Reacts to all messages posted in the GENERAL channel with a pre-defined list of emojis
    def react_announcement(self, message_json):
        if self.GENERAL_CHANNEL != "" and message_json["channel"] == self.GENERAL_CHANNEL:
            temp_list = list(self.EMOJI_LIST)
            Bot.emoji_reaction(self, message_json["channel"], message_json["ts"], "pantherbot")
            for x in range(0, 3):
                num = random.randrange(0, len(temp_list))
                Bot.emoji_reaction(self, message_json["channel"], message_json["ts"], temp_list.pop(num))

    def log_event(self, response):
        def add_user(r, team_join=False):
            users_with_this_slack_id = self.ENGINE.execute("SELECT last_name FROM users WHERE slack_id=%s", r["user"])
            if users_with_this_slack_id.fetchall() == []:
                r = self.SLACK_CLIENT.api_call(
                    "users.info",
                    user=r["user"]
                    )
                is_admin = r["user"]["is_admin"]
                if is_admin:
                    is_admin = 1
                else:
                    is_admin = 0
                if team_join==True:
                    self.ENGINE.execute("INSERT INTO users (slack_id, first_name, last_name, is_admin, is_pb_admin, team_join) VALUES (%s, %s, %s, "+str(is_admin)+", 0, CURDATE())", r["user"]["id"], r["user"]["profile"]["first_name"], r["user"]["profile"]["last_name"])
                else:
                    self.ENGINE.execute("INSERT INTO users (slack_id, first_name, last_name, is_admin, is_pb_admin) VALUES (%s, %s, %s, "+str(is_admin)+", 0)", r["user"]["id"], r["user"]["profile"]["first_name"], r["user"]["profile"]["last_name"])

        def add_channel(r):
            if r.has_key("channel"):
                q = self.ENGINE.execute("SELECT name FROM channels WHERE slack_id=%s", r["channel"])
            else:
                q = self.ENGINE.execute("SELECT name FROM channels WHERE slack_id=%s", r["item"]["channel"])
            if q.fetchall() == []:
                r = self.SLACK_CLIENT.api_call(
                        "channels.info",
                        channel=r["channel"]
                    )
                self.ENGINE.execute("INSERT INTO channels (slack_id, name, is_productive, is_active) VALUES (%s, %s, 0, 1)", r["channel"]["id"], r["channel"]["name"])

        if response["type"] == "message":
            add_user(response)
            add_channel(response)
            self.ENGINE.execute("INSERT IGNORE INTO commentActivity (from_user_id, to_channel_id, comment_count) VALUES (%s, %s, 0)", response["user"], response["channel"])
            self.ENGINE.execute("UPDATE commentActivity SET comment_count = comment_count+1 WHERE from_user_id = %s and to_channel_id = %s", response["user"], response["channel"])
            now = datetime.datetime.now()
            self.ENGINE.execute("INSERT INTO channelActivity (channel_id, hour, week_day, day_of_month, month, year) VALUES (%s, %s, %s, %s, %s, %s)", response["channel"], now.hour, now.strftime("%a")[:2], now.day, now.month, now.year)
            return
            
        if response["type"] == "team_join":
            add_user(response, team_join=True)
            return
        
        if response["type"] == "reaction_added":
            if response["item"]["type"] == "message":
                reaction = response["reaction"]
                if len(reaction) > 60:
                    reaction = reaction[:60]
                add_user(response)
                add_channel(response)
                self.ENGINE.execute("INSERT IGNORE INTO emojis (name, is_custom) VALUES (%s, 0)", reaction)
                self.ENGINE.execute("INSERT IGNORE INTO emojiActivity (from_user_id, to_user_id, in_channel_id, emoji_name, given_count) VALUES(%s, %s, %s, %s, 0)", response["user"], response["item_user"], response["item"]["channel"], reaction)
                self.ENGINE.execute("UPDATE emojiActivity SET given_count = given_count+1 WHERE from_user_id = %s and to_user_id = %s and in_channel_id = %s and emoji_name = %s", response["user"], response["item_user"], response["item"]["channel"], reaction)
            return

        if response["type"] == "reaction_removed":
            if response["item"]["type"] == "message":
                reaction = response["reaction"]
                if len(reaction) > 60:
                    reaction = reaction[:60]
                add_user(response)
                add_channel(response)
                self.ENGINE.execute("INSERT IGNORE INTO emojis (name, is_custom) VALUES (%s, 0)", reaction)
                self.ENGINE.execute("INSERT IGNORE INTO emojiActivity (from_user_id, to_user_id, in_channel_id, emoji_name, given_count) VALUES(%s, %s, %s, %s, 0)", response["user"], response["item_user"], response["item"]["channel"], reaction)
                self.ENGINE.execute("UPDATE emojiActivity SET given_count = given_count-1 WHERE from_user_id = %s and to_user_id = %s and in_channel_id = %s and emoji_name = %s", response["user"], response["item_user"], response["item"]["channel"], reaction)
            return

        if response["type"] == "channel_created":
            self.ENGINE.execute("INSERT IGNORE INTO channels (slack_id, name, is_productive, is_active) VALUES (%s, %s, 0, 1)", response["channel"]["id"], response["channel"]["name"])
            return

        if response["type"] == "channel_archive":
            add_channel(response)
            self.ENGINE.execute("UPDATE channels SET is_active = 0 WHERE slack_id = %s", response["channel"])
            return

        if response["type"] == "channel_unarchive":
            add_channel(response)
            self.ENGINE.execute("UPDATE channels SET is_active = 1 WHERE slack_id = %s", response["channel"])
            return

    def setup_tables(self):
        try:
            print 'PantherBot:LOG:Attempting to connect to database'
            self.ENGINE.connect()
        except Exception:
            print 'PantherBot:LOG:Could not find database'
            print 'PantherBot:LOG:Creating database'
            self.ENGINE = create_engine('mysql://root@localhost:3306')
            self.ENGINE.execute("CREATE DATABASE pantherbot_test")
            self.ENGINE.execute("USE pantherbot_test")
            self.ENGINE.execute("CREATE TABLE channels(slack_id VARCHAR(9), name VARCHAR (50), is_productive TINYINT, is_active TINYINT, PRIMARY KEY (slack_id))")
            self.ENGINE.execute("CREATE TABLE users(slack_id VARCHAR(9), first_name VARCHAR(40), last_name VARCHAR(40), join_date DATETIME, is_admin TINYINT, is_pb_admin TINYINT, PRIMARY KEY (slack_id))")
            self.ENGINE.execute("CREATE TABLE emojis(name VARCHAR(60), is_custom TINYINT, PRIMARY KEY (name))")
            self.ENGINE.execute("CREATE TABLE commentActivity(from_user_id VARCHAR(9), to_channel_id VARCHAR(9), comment_count INTEGER, PRIMARY KEY (from_user_id, to_channel_id), FOREIGN KEY (from_user_id) REFERENCES users (slack_id), FOREIGN KEY (to_channel_id) REFERENCES channels (slack_id))")
            self.ENGINE.execute("CREATE TABLE emojiActivity(from_user_id VARCHAR(9), to_user_id VARCHAR(9), in_channel_id VARCHAR(9), emoji_name VARCHAR(60), given_count INTEGER, PRIMARY KEY (from_user_id, to_user_id, in_channel_id, emoji_name),  FOREIGN KEY (from_user_id) REFERENCES users (slack_id), FOREIGN KEY (to_user_id) REFERENCES users (slack_id), FOREIGN KEY (in_channel_id) REFERENCES channels (slack_id))")    
            self.ENGINE.execute("CREATE TABLE channelActivity(channel_id VARCHAR(9), hour TINYINT, week_day VARCHAR(2), day_of_month TINYINT, month TINYINT, year SMALLINT, FOREIGN KEY (channel_id) REFERENCES channels (slack_id))")
        finally:
            print 'PantherBot:LOG:Connected to database'

    def riyans_denial(self, message_json):
        if "U0LJJ7413" in message_json["user"]:
            if message_json["text"][:1] in ["!", "$"] or message_json["text"].lower() in ["hey pantherbot", "pantherbot ping"]: 
                self.response_message(message_json, ["No."])
                return True
        return False