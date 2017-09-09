#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, json
import sys
from response import Response

from pb_logging import PBLogger
logger = PBLogger("CatFact")

def run(response):
    response_obj = Response(sys.modules[__name__])
    try:
        web_page_contents = urllib2.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read()
        parsed_wbc = json.loads(web_page_contents)
        
        response_obj.messages_to_send.append(parsed_wbc["facts"][0])
        
    except Exception as e:
        logger.error("Error in catfacts: " + str(e)) 
        response_obj.status_code = -1
    
    return response_obj   

def return_alias():
    alias_list = ["catfact"]
    return alias_list

def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("Cat facts can't be returned right now :sob:")
    else:
        response_obj.messages_to_send.append("An unknown error occured. Error code: " + error_code)
    return response_obj

def is_admin_command():
    return False

def help_preview():
    return "!catfact"

def help_text():
    return "Catfact returns a random catfact from a lovely API that crashes all the time. Praise Lord Mittens. Ask about Mo's cats."