#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess, platform, os 
import sys
from response import Response

from pb_logging import PBLogger

logger = PBLogger("Admin")

def run(message_json, args, sc, bot, rmsg):
    response_obj = Response(sys.modules[__name__])
    if args[0].lower() == "add":
        args.pop(0)
        admin_add(message_json, args, sc, bot, rmsg)
    return response_obj

def return_alias():
    alias_list = ["admin"]
    return alias_list

# Temporary function to add Admins for testing purposes
def admin_add(message_json, args, sc, bot, rmsg):
    
    for id in args:
        bot.ADMIN.append(id)
        rmsg(message_json, ["User ID " + id + " has been temporarily added to the admin list"])
        logger.info("User ID " + id + "has been temporarily added to the admin list")

def is_admin_command():
    return True

def help_preview():
    return "$admin add"

def help_text():
    return "$admin allows for moderator intervention to the live instance of PantherBot. Currently this just means adding more admins to the list, but that will change in the future."