#!/usr/bin/env python
# -*- coding: utf-8 -*-
import upsidedown
import sys
from response import Response

# flips text using upsidedown module and has a donger for emohasis
def rage(response, args=[]):
    response_obj = Response(sys.modules[__name__])
    toFlip = ''
    donger = '(ノಠ益ಠ)ノ彡'
    for n in range(0, len(args)):
        toFlip += args[n] + " "

    if toFlip == '':
        toFlip = unicode('┻━┻', "utf-8")

    try:
        donger = unicode(donger, "utf-8")
        flippedmsg = upsidedown.transform(toFlip)
        response_obj.messages_to_send.append(donger + flippedmsg)
    except Exception as e:
        logger.info("[Rage] Error in flip: " + str(e))
        response_obj.messages_to_send.append("Sorry, I can't seem to flip right now, or you gave an invalid argument")
    return response_obj

def is_admin_command():
    return False