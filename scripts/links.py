#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Links")

# flips a coin
def run(response, args):
    response_obj = Response(sys.modules[__name__])
    res_message = ""
    links = {
        "Website":"pantherhackers.com",
        "Slack":"pantherhackers.slack.com",
        "Instagram":"instagram.com/pantherhackers",
        "Twitter":"twitter.com/pantherhackers",
        "GitHub":"github.com/PantherHackers"
    }
    specific_link = False
    if args:
        specific_link = True
    if specific_link:
        try:
            for a in args:
                res_message = res_message + a.lower().capitalize() + ": " + links[a.lower().capitalize()] + "\n"
        except Exception as e:
            logger.error(a.lower().capitalize() + " not found in links")
            specific_link = False
            break
    if not specific_link:
        res_message = ""
        for n, l in links:
            res_message = res_message + n + ": " + l + "\n"
    response_obj.messages_to_send.append(res_message)
    logger.info(res_message)
    return response_obj

def return_alias():
    alias_list = ["links"]
    return alias_list

def is_admin_command():
    return False

def help_preview():
    return "!links <Optional:String>"

def help_text():
    return "Lists links to revelant pages and social accounts."
