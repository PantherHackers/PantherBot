#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Coin")

# flips a coin
def coin(response):
    response_obj = Response(sys.modules[__name__])
    l = ["Heads", "Tails"]
    m = random.randrange(0, 2)
    response_obj.messages_to_send.append(l[m])
    logger.info(l[m])
    return response_obj

def is_admin_command():
    return False