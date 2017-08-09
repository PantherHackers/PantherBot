#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
from response import Response

# flips a coin
def run(response):
    response_obj = Response(sys.modules[__name__])
    l = ["Heads", "Tails"]
    m = random.randrange(0, 2)
    response_obj.messages_to_send.append(l[m])
    return response_obj

def return_alias():
    alias_list = ["coin"]
    return alias_list

def is_admin_command():
    return False