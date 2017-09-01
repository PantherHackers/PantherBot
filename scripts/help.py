#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Help")

# help script that details the list of commands
def run(response):
    response_obj = Response(sys.modules[__name__])
    text = "PantherBot works by prefacing commands with \"!\"\n"
    text += "Commands:\n"
    text += "```!help or !h\n"
    text += "!coin\n"
    text += "!helloworld\n"
    text += "!version\n"
    text += "!fortune\n"
    text += "!conch or !magicconch\n"
    text += "!flip <Optional:String>\n"
    text += "!unflip <Optional:String>\n"
    text += "!rage <Optional:String>\n"
    text += "!catfact\n"
    text += "!pugbomb <int>\n"
    text += "!taskme\n"
    text += "!poll <begin/start/end/results> [arguments followed by a `;`]"
    text += "!talk <String>\n"
    text += "\"Hey PantherBot\"```\n"
    text += "Try saying `Hey PantherBot` or `!coin`"

    motext = "Admins are able to use admin commands prefaced with \"$\"\n"
    motext += "```$calendar add ; <Title> ; <Date in format YYYY-MM-DD> ; <Start time in format HH:mm> ; <End time in format HH:mm> ; <Description> ; <Location>\n"  # noqa: 501
    motext += "$admin <reconnect/update>\n"
    motext += "$log <true/false> <channels>```\n"
    motext += "Got suggestions for PantherBot? Fill out our typeform to leave your ideas! https://goo.gl/rEb0B7"  # noqa: 501
    response_obj.messages_to_send.append(text)
    response_obj.messages_to_send.append(motext)
    logger.info("Help response")
    return response_obj

def return_alias():
    alias_list = ["help", "h"]
    return alias_list

def is_admin_command():
    return False