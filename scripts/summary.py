#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
import urllib2, json
from response import Response

from pb_logging import PBLogger
logger = PBLogger("Summary")

# flips a coin
def run(response, args):
    response_obj = Response(sys.modules[__name__])
    res_text = ""
    if args:
        smmry_url = "http://api.smmry.com/&SM_API_KEY=CFE8330DFD&SM_URL=" + args[0]
        parsed_response = json.loads(urllib2.urlopen(smmry_url).read())
        if 'sm_api_content' in parsed_response:
            res_text = parsed_response['sm_api_content']
        else:
            res_text = "Whoops, something went wrong with the SMMRY API"
    else:
        res_text = "D'oh, you didn't include a link!"
    response_obj.messages_to_send.append(res_text)
    logger.info(res_text)
    return response_obj

def return_alias():
    alias_list = ["summary"]
    return alias_list

def is_admin_command():
    return False

def help_preview():
    return "!summary <url>"

def help_text():
    return "Get a summary of an article or webpage"
