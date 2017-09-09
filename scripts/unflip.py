#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Unflip")

#"unflips" text
def run(response, args=[]):
    response_obj = Response(sys.modules[__name__])
    toUnFlip = ''
    for n in range(0, len(args)):
        toUnFlip += args[n] + " "

    if toUnFlip == "":
        toUnFlip = unicode('┬──┬', "utf-8")

    try:
        donger = "ノ( º _ ºノ)"
        donger = unicode(donger, "utf-8")
        logger.info(toUnFlip[:15 or len(toUnFlip)] + "...")
        response_obj.messages_to_send.append(toUnFlip + donger)
    except Exception as e:
        logger.error("Error in flip: " + str(e))
        response_obj.status_code = -1
    return response_obj

def return_alias():
    alias_list = ["unflip"]
    return alias_list

def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("Sorry, there seems to have been an error while unflipping. Take this donger instead: (╯°□°)╯︵┻━┻")
    else:
        response_obj.messages_to_send.append("An unknown error occured. Error code: " + error_code)
    return response_obj

def is_admin_command():
    return False

def help_preview():
    return "!unflip <Optional:String>"

def help_text():
    return "Restore order to the world by placing the table or text back down. I'm proud of you citizen!"