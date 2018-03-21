#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, json
import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Fortune")

# returns a random "fortune"
def run(response, args=None):
    response_obj = Response(sys.modules[__name__])
    fortune_url = "https://9bj8bks4p3.execute-api.us-west-2.amazonaws.com/prod/fortunefortoday-get-cookie" # This was the URL I found in the JS code on the website

    try:
        # get fortune
        raw_response = urllib2.urlopen(fortune_url).read()
        parsed_response = json.loads(raw_response)
        fortune = parsed_response['body-json']['GetCookieResult'] # The JSON returned is pretty weird, this is where it stores the actual fortune

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

def help_preview():
    return "!fortune"

def help_text():
    return "Returns a random fortune from an inconsistent API. Responses are slow, just give it some time Jim!"
