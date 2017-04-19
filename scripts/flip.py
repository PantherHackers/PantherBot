#!/usr/bin/env python
# -*- coding: utf-8 -*-
import upsidedown, sys
from response import Response

# flips text using upsidedown module and has a donger for emohasis
def flip(response, args=[]):
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
        flippedmsg = upsidedown.transform(toFlip)
        response_obj.messages_to_send.append(donger + flippedmsg)
    except Exception as e:
        print "PantherBot:Log:Flip:Error in flip: " + str(e)
        response_obj.status_code = -1
    return response_obj


def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("Sorry, there seems to have been an error while flipping. Take this donger instead: (╯°□°)╯︵┻━┻")
    else:
        response_obj.messages_to_send.append("An unknown error occured. Error code: " + error_code)
    return response_obj

def is_admin_command():
    return False