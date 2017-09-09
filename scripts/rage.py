#!/usr/bin/env python
# -*- coding: utf-8 -*-
import upsidedown
import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Rage")

# flips text using upsidedown module and has a donger for emohasis
def run(response, args=[]):
    response_obj = Response(sys.modules[__name__])
    toFlip = ''
    donger = '(ノಠ益ಠ)ノ彡'
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
        logger.error("Error in flip: " + str(e))
        response_obj.messages_to_send.append("Sorry, I can't seem to flip right now, or you gave an invalid argument")
    return response_obj

def return_alias():
    alias_list = ["rage"]
    return alias_list

def is_admin_command():
    return False

def help_preview():
    return "!rage <Optional:String>"

def help_text():
    return "Rage flips the text or table because you really want the world to know that you're upset."