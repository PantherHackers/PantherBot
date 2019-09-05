#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Links")

# flips a coin
def run(response):
    response_obj = Response(sys.modules[__name__])
    res_message = ""
    links = {
        "Website":"pantherhackers.com",
        "Slack":"pantherhackers.slack.com",
        "Instagram":"instagram.com/pantherhackers",
        "Twitter":"twitter.com/pantherhackers",
        "GitHub":"github.com/PantherHackers"
    }
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
    return "!links"

def help_text():
    return "Lists links to revelant pages and social accounts."
