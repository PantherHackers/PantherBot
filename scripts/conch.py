#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Conch")

# flips a coin
def run(response, args):
    response_obj = Response(sys.modules[__name__])
    lower_args = [arg.lower() for arg in args]
    if "or" in lower_args:
        l = ["Neither."]
    else:
        l = ["Yes.", "No.", "Maybe someday.", "I don't think so.", "Follow the seahorse.", "Try asking again."]
    m = random.randrange(0, len(l))
    response_obj.messages_to_send.append(l[m])
    logger.info(l[m])
    return response_obj

def return_alias():
    alias_list = ["conch", "magicconch"]
    return alias_list

def is_admin_command():
    return False