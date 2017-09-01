#!/usr/bin/env python
# -*- coding: utf-8 -*-
import upsidedown, sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Flip")

# flips text using upsidedown module and has a donger for emohasis
def run(response, args=[]):
    response_obj = Response(sys.modules[__name__])
    toFlip = ''
    donger = '(╯°□°)╯︵'
    if len(args) >= 0:
        for n in range(0, len(args)):
            toFlip += args[n] + " "

    if toFlip == '':
        toFlip = unicode('┻━┻', "utf-8")

    try:
        donger = unicode(donger, "utf-8")
        logger.info(toFlip[:15 or len(toFlip)] + "...")
        flippedmsg = upsidedown.transform(toFlip)
        response_obj.messages_to_send.append(donger + flippedmsg)
    except Exception as e:
        logger.error(str(e))
        response_obj.status_code = -1
    return response_obj

def return_alias():
    alias_list = ["flip"]
    return alias_list

def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("Sorry, there seems to have been an error while flipping. Take this donger instead: (╯°□°)╯︵┻━┻")
    else:
        response_obj.messages_to_send.append("An unknown error occured. Error code: " + error_code)
    return response_obj

def is_admin_command():
    return False

def help_preview():
    return "!flip <Optional:String>"

def help_text():
    return unicode("Flips your message because sometimes you just really need someone to know that they messed up... Or your DM is having you face a dragon and want to spare your favorite character. (╯°□°)╯︵┻━┻", "utf-8")