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
import threading, websocket, json, re, time, codecs, random
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
            print "PantherBot:LOG:Initializing WebSocketApplication"
            self.WEBSOCKET = websocket.WebSocketApp(bot_conn["url"],
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    on_open=self.on_open)

    def initialize_info(self):
        # Update current USER_LIST (since members may join while PantherBot is off, its safe to make an API call every initial run)
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

    def on_message(self, ws, message):
        message_thread = threading.Thread(target=self.on_message_thread, args=(message,))
        self.THREADS.append(message_thread)
        message_thread.start()
        return

    def on_message_thread(self, message):
        s = message.decode('utf-8')
        message_json = json.loads(unicode(s))
        print "PantherBot:LOG:message:" + message_json["type"]
        
        if "message" == message_json["type"]:
            if "subtype" in message_json:
                if message_json["subtype"] == "bot_message":
                    #polling logic
                    if "POLL_BEGIN" in message_json["text"]:
                        self.POLLING_LIST[message_json["channel"]][0] = message_json["ts"]
                        temp_options = self.POLLING_LIST[message_json["channel"]][1]
                        for key in temp_options:
                            rreaction(message_json, temp_options[key].strip(":"))
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
        self.smsg("pantherbot-dev", "Bot successfully started")

    # message_json Message
    # Sends a message to the same channel that message_json originates from
    def rmsg(self, message_json, l):
        for text in l:
            self.SC.api_call(
                "chat.postMessage",
                channel=message_json["channel"],
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
    # Returns True if a message_json or trigger was used in this method
    def command_message(self, message_json):
        # Checks if message starts with an exclamation point, and does the respective task 
        if message_json["text"][:1] == "!":
            # Put all ! command parameters into an array
            args = message_json["text"].split()
            com_text = args[0][1:].lower()
            args.pop(0)  # gets rid of the command

            # Checks if command is an Admin command
            if com_text in self.ADMIN_COMMANDS:
                self.rmsg(message_json, ["Sorry, admin commands may only be used with the $ symbol (ie. `$admin`)"]) 
                return True

            if com_text == "version":
                self.rmsg(message_json, [self.VERSION])
                return True

            if com_text == "talk":
                ch = self.channels_to_ids([TTPB])
                c = ch[0]
                if message_json["channel"] != c:
                    self.rmsg(message_json, ["Talk to me in #" + TTPB])
                    return True

            if com_text[0] == '!':
                return True

            # list that contains the message_json and args for all methods
            method_args = []
            method_args.append(message_json)

            if com_text == "poll":
                method_args.append(polling_list[message_json["channel"]])
                method_args.append(sc)

            if len(args) > 0:
                method_args.append(args)
            # Attempts to find a command with the name matching the command given, and executes it
            # try:
            called_function = getattr(commands[com_text], com_text)
            script_response = called_function(*method_args)
            if script_response.status_code is 0:
                self.rmsg(message_json, script_response.messages_to_send)
            else:
                error_cleanup = getattr(script_response.module_called, "error_cleanup")
                error_response = error_cleanup(script_response.status_code)
                self.rmsg(message_json, error_response.messages_to_send)
            return True
            # except:
            #     # If it fails, outputs that no command was found or syntax was broken.
            #     self.rmsg(message_json, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])
            #     return True
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

                if message_json["user"] in self.ADMIN:
                    l = []
                    l.append(message_json)
                    l.append(args)
                    l.append(self.SC)
                    l.append(self.rmsg)
                    try:
                        f = getattr(commands[com_text], com_text)
                        f(*l)
                        return True
                    except:
                        self.rmsg(message_json, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])
                        return True

                # Checks if command is an admin command
                elif com_text in self.ADMIN_COMMANDS:
                    self.rmsg(message_json, ["It seems you aren't authorized to use admin commands. If you believe this a mistake, contact the maintainer(s) of PantherBot"])
                    return True
                else:
                    self.rmsg(message_json, ["You seem to have used a function that doesnt exist, or used it incorrectly. See `!help` for a list of functions and parameters"])

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


def check_log():
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
    ADMIN = os.environ.get('ADMIN_LIST')
    if ADMIN is None:
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
        NEWUSERGREETING = True
    GREETING = target.readline().rstrip('\n')
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
                t = os.environ.get('SLACK_SECRET')
                if t is None:
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

    # Other Messages are messages that don't follow standard conventions (such as "Hey PantherBot!")
    # Returns True if a message_json or trigger was used in this method
    def other_message(self, message_json):
        # If not an ! or $, checks if it should respond to another message format, like a greeting 
        try:
            if re.match(".*panther +hackers.*", str(message_json["text"].lower())):
                self.rmsg(message_json, ["NO THIS IS PANTHERHACKERS"])
                return True
            elif message_json["text"].lower() == "hey pantherbot":
                # returns user info that said hey
                # TODO make this use USER_LIST
                temp_user = self.SC.api_call(
                    "users.info",
                    user = message_json["user"]
                )
                print "PantherBot:LOG:Greeting:We did it reddit"
                self.rmsg(message_json, ["Hello, " + temp_user["user"]["profile"]["first_name"] + "! :tada:"])
                return True
            elif message_json["text"].lower() == "pantherbot ping":
                self.rmsg(message_json, ["PONG"])
                return True
            elif message_json["text"].lower() == ":rip: pantherbot" or message_json["text"].lower() == "rip pantherbot":
                self.rmsg(message_json, [":rip:"])
                return True
            elif re.match(".*panther +hackers.*", str(message_json["text"].lower())):
                self.rmsg(message_json, ["NO THIS IS PANTHERHACKERS"])
                return True
            elif "subtype" in message_json:
                if message_json["subtype"] == "channel_leave" or message_json["subtype"] == "group_leave": 
                    self.rmsg(message_json, ["Press F to pay respects"])
                    return True
            return False
        except:
            print "Error with checking in other_message: likely the message contained unicode characters"

    # Reacts to all messages posted in the GENERAL channel with a pre-defined list of emojis
    def react_announcement(self, message_json):
        if self.GENERAL_CHANNEL != "" and message_json["channel"] == self.GENERAL_CHANNEL:
            temp_list = list(self.EMOJI_LIST)
            self.rreaction(message_json, "pantherbot")
            for x in range(0, 3):
                num = random.randrange(0, len(temp_list))
                self.rreaction(message_json, temp_list.pop(num))

    def rreaction(self, message_json, emoji):
        self.SC.api_call(
            "reactions.add",
            name=emoji,
            channel=message_json["channel"],
            timestamp=message_json["ts"]
        )
        print "PantherBot:LOG:Reaction posted"

    def riyans_denial(self, message_json):
        if "U0LJJ7413" in message_json["user"]:
            if message_json["text"][:1] in ["!", "$"] or message_json["text"].lower() in ["hey pantherbot", "pantherbot ping"]: 
                self.rmsg(message_json, ["No."])
                return True
        return False
