#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess, platform, os 
import sys
from response import Response


def admin(message_json, args, sc, bot, rmsg):
    response_obj = Response(sys.modules[__name__])
    if args[0].lower() == "add":
        args.pop(0)
        admin_add(message_json, args, sc, bot, rmsg)
    return response_obj


# Temporary function to add Admins for testing purposes
def admin_add(message_json, args, sc, bot, rmsg):
    print "Adding user to admin list temporarily"
    for id in args:
        bot.ADMIN.append(id)
        rmsg(message_json, ["User ID " + id + " has been temporarily added to the admin list"])

def is_admin_command():
    return True