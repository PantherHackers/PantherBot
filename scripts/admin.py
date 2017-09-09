#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, json
import sys
from response import Response
from slackclient import SlackClient

from pb_logging import PBLogger

logger = PBLogger("Admin")

def run(message_json, args, sc, bot, rmsg):
    response_obj = Response(sys.modules[__name__])
    if args[0].lower() == "list":
        logger.info("Admin command list")
        response_obj.messages_to_send.append("The current admin commands are `list`, `add`, and `inactive-list`")
    elif args[0].lower() == "add":
        logger.info("Add admin")
        args.pop(0)
        admin_add(message_json, args, sc, bot, rmsg) 
    # This requires the user's token be authed as admin (legacy, not bot tokens bypass this need)
    elif args[0].lower() == "inactive-list":
        logger.info("Inactive list")
        args.pop(0)
        response_obj = compile_inactive_list(message_json, bot, response_obj)
    else:
        logger.info("No admin command called for")
        response_obj.messages_to_send.append("The argument `" + args[0] + "` is not a proper admin command.")
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
    list_of_emails = check_user_status(bot)
    response_obj.messages_to_send.append("Sending list to you in a DM.")
    message_string = "List of emails:\n"
    for email in list_of_emails:
        message_string += email + "\n"
    bot.message_user(message_json["user"], message_string)
    return response_obj

# Checks the user list for activity in the last 14 days, and return a list of emails.
def check_user_status(bot):
    temp_list = bot.SLACK_CLIENT.api_call(
        "team.billableInfo"
    )
    if temp_list["ok"] is not True:
        logger.error("User token likely not authed with admin scope. Please update use a legacy token, or use the proper OAuth request.")
        return ["List is unobtainable with current token auth scope."]
    data = temp_list["billable_info"]
    list_of_marked_users = []
    list_of_emails = []
    for user in data:
        if data[user]["billing_active"] is False:
            list_of_marked_users.append(user)

    for user in bot.BOT_CONN["users"]:
        if user["id"] in list_of_marked_users:
            try:
                list_of_emails.append(user["profile"]["email"])
            except:
                logger.info("No email available for user: " + user["name"])

    logger.info("User list checked. " + str(len(list_of_marked_users)) + " have been marked as inactive in the last 14 days.")
    return list_of_emails

def is_admin_command():
    return True

def help_preview():
    return "$admin add"

def help_text():
    return "$admin allows for moderator intervention to the live instance of PantherBot. Currently this just means adding more admins to the list, but that will change in the future."