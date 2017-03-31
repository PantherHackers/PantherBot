#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
from response import Response

# flips a coin
def coin(response):
    response_obj = Response(sys.modules[__name__])
    l = ["Heads", "Tails"]
    m = random.randrange(0, 2)
    response_obj.messages_to_send.append(l[m])
    return response_obj
