#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from response import Response

#"unflips" text
def unflip(response, args=[]):
    response_obj = Response(sys.modules[__name__])
    toUnFlip = ''
    for n in range(0, len(args)):
        toUnFlip += args[n] + " "

    if toUnFlip == "":
        toUnFlip = unicode('┬──┬', "utf-8")

    try:
        donger = "ノ( º _ ºノ)"
        donger = unicode(donger, "utf-8")
        response_obj.messages_to_send.append(toUnFlip + donger)
    except Exception as e:
        print "PantherBot:Log:Flip:Error in flip: " + str(e)
        response_obj.status_code = -1
    return response_obj

def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("Sorry, there seems to have been an error while unflipping. Take this donger instead: (╯°□°)╯︵┻━┻")
    else:
        response_obj.messages_to_send.append("An unknown error occured. Error code: " + error_code)
    return response_obj

def is_admin_command():
    return False