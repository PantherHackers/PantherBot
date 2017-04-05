#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess, platform, os 
import sys
from response import Response


def admin(message_json, args, sc, bot, rmsg):
    response_obj = Response(sys.modules[__name__])
    if args[0].lower() == "update":
        update_bot(message_json, rmsg)
    if args[0].lower() == "add":
        admin_add(message_json, bot, rmsg)
    return response_obj


# Update function for PantherBot so it clones latest master, replaces directories, and restarts. Currently not functional  # noqa: 501
def update_bot(message_json, rmsg):
    print "PantherBot:LOG:Updating..."
    rmsg(message_json, ["Updating..."])
    script_dir = os.path.dirname(os.path.dirname(__file__))
    proc = subprocess.Popen("./update.sh", cwd=script_dir, shell=True)

# Temporary function to add Admins for testing purposes
def admin_add(message_json, args, sc, bot, rmsg):
    print "Adding user to admin list temporarily"
    for id in args:
        bot.ADMIN.append(id)
        rmsg(message_json, ["User ID " + id + " has been temporarily added to the admin list"])

def is_admin_command():
    return True