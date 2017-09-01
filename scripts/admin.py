#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time
import sys
from response import Response

from pb_logging import PBLogger

logger = PBLogger("Admin")

def run(message_json, args, sc, bot, rmsg):
    response_obj = Response(sys.modules[__name__])
    if args[0].lower() == "add":
        logger.info("Add admin")
        args.pop(0)
        admin_add(message_json, args, sc, bot, rmsg)
    elif args[0].lower() == "inactive-list":
        logger.info("Inactive list")
        args.pop(0)
        response_obj = compile_inactive_list(message_json, bot, response_obj)
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

def compile_inactive_list(message_json, bot, response_obj):
    list_of_marked_users = check_user_status(bot)
    response_obj.messages_to_send.append("Sending list to you in a DM.")
    message_string = "List of emails:\n"
    for email in list_of_marked_users:
        message_string += email + "\n"
    bot.message_user(message_json["user"], message_string)
    return response_obj

# Checks the user list for activity in the last 30 days, and return a list of emails.
def check_user_status(bot):
    temp_list = bot.SLACK_CLIENT.api_call(
        "users.list"
    )
    list_of_marked_users = []
    for user in temp_list["members"]:
        user_updated_ts = float(user["updated"])
        current_ts = time.time()
        if user_updated_ts < (current_ts - 10):
            list_of_marked_users.append(user["profile"]["email"])
    logger.info("User list checked. " + str(len(list_of_marked_users)) + " have been marked as inactive in the last 30 days.")
    return list_of_marked_users


def is_admin_command():
    return True

def help_preview():
    return "$admin add"

def help_text():
    return "$admin allows for moderator intervention to the live instance of PantherBot. Currently this just means adding more admins to the list, but that will change in the future."