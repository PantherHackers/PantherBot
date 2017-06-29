#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import sys
from response import Response

import log_handler

# returns a random "fortune"
def fortune(response):
    response_obj = Response(sys.modules[__name__])
    try:
        # get fortune
        fortune = urllib2.urlopen("http://www.fortunefortoday.com/getfortuneonly.php").read()  # noqa: 501
    except:
        fortune = "Unable to reach fortune telling api"
        logger.error("[Fortune] Error in receiving fortune")

    # make api call
    response_obj.messages_to_send.append(fortune)
    return response_obj

def is_admin_command():
    return False