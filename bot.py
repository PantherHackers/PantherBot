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
    pbCooldown (int): Global Variable

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from slackclient import SlackClient

import threading, websocket, json, re, time, codecs, random, os
import scripts
from scripts import commands

import log_handler
import logging 

logger = logging.getLogger('Bot')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler.PBLogHandler())    

class Bot(object):
    # admin_env_string = os.environ['PB_ADMIN']
    # ADMIN = admin_env_string.split(',')

    # Set the name for the logger
    # Add custom log handler to logger

    EMOJI_LIST = ["party-parrot", "venezuela-parrot", "star2", "fiesta-parrot", "wasfi_dust", "dab"]
    GENERAL_CHANNEL = ""
    TTPB = "talk-to-pantherbot"
    VERSION = "2.0.0"

    def __init__(self, token, bot_name=""):
        self.SLACK_CLIENT = None
        self.BOT_NAME = bot_name
        self.BOT_ICON_URL = "http://i.imgur.com/QKaLCX7.png"
        self.USER_LIST = None
        self.POLLING_LIST = dict()
        self.WEBSOCKET = None
        self.THREADS = []
        self.pb_cooldown = True
        self.create_slack_client(token)

    def create_slack_client(self, token):
    	self.SLACK_CLIENT = SlackClient(token)

    # Returns a list of channel IDs searched for by name
    def channels_to_ids(self, channel_names):
        pub_channels = self.SLACK_CLIENT.api_call(
            "channels.list",
            exclude_archived=1
        )
        pri_channels = self.SLACK_CLIENT.api_call(
            "groups.list",
            exclude_archived=1
        )
        list_of_channels = []
        for channel in pub_channels["channels"]:
            for num in range(0, len(channel_names)):
                if channel["name"].lower() == channel_names[num].lower():
                    list_of_channels.append(channel["id"])
        # Same as above
        for channel in pri_channels["groups"]:
            for num in range(0, len(channel_names)):
                if channel["name"].lower() == channel_names[num].lower():
                    list_of_channels.append(channel["id"])
        return list_of_channels

    # Send Message
    # Sends a message to the specified channel (looks up by channel name, unless is_id is True)
    def send_msg(self, channel, text, is_id=False):
        if is_id:
            channel_id = channel
        else:
            channel_id = self.channels_to_ids([channel])[0]
        self.SLACK_CLIENT.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=text,
            username=self.BOT_NAME,
            icon_url=self.BOT_ICON_URL
        )
        logger.info("Message sent")

    def emoji_reaction(self, channel, ts, emoji):
        self.SLACK_CLIENT.api_call(
            "reactions.add",
            name=emoji,
            channel=channel,
            timestamp=ts
        )
        logger.info("Reaction posted")

    def close(self):
        self.WEBSOCKET.keep_running = False