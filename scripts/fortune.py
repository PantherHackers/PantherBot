#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Fortune")

# returns a random "fortune"
def run(response):
    response_obj = Response(sys.modules[__name__])
    try:
        # get fortune
        fortune = urllib2.urlopen("http://www.fortunefortoday.com/getfortuneonly.php").read()  # noqa: 501
    except Exception as e:
        fortune = "Unable to reach Fortune Telling api"
        logger.error("Unable to reach Fortune Telling API: " + str(e))

    # make api call
    response_obj.messages_to_send.append(fortune)
    return response_obj

def return_alias():
    alias_list = ["fortune"]
    return alias_list

def is_admin_command():
    return False