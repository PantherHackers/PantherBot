#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import sys
from response import Response

def run(response, pb_cooldown, args=None):
    response_obj = Response(sys.modules[__name__])
    
    if pb_cooldown is False:
        response_obj.messages_to_send.append("Sorry, reddit is on cooldown.")
        return response_obj
    
    reddit = praw.Reddit(client_id='aGpQJujCarDHWA',
                        client_secret='fkA9lp0NDx23B_qdFezTeGyGKu8',
                        user_agent='my user agent',
                        password='PHGSU2017',
                        username='Panther_Bot')
    subreddit = "GaState"
    
    if args is not None: # Use specified subreddit. Else, default to r/GaState
        subreddit = str(args[0])
        if subreddit.startswith("r/"):
            subreddit = subreddit[2:]
    
    post_urls=[]
    for submission in reddit.subreddit(subreddit).hot(limit=3):
        post_urls.append(submission.url)
    response_obj.messages_to_send = post_urls
    response_obj.special_condition = True
    return response_obj

def return_alias():
    alias_list = ["reddit"]
    return alias_list

def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    response_obj.messages_to_send.append("An unknown error occured. Error code: " + str(error_code))
    return response_obj

def set_cooldown(bot):
    if bot.pb_cooldown is True:
        bot.pb_cooldown = False

def special_condition(bot):
    set_cooldown(bot)

def is_admin_command():
    return False

def help_preview():
    return "!reddit"

def help_text():
    return "Returns top 3 hot posts from a subreddit (Defaults to r/GaState if no subreddit provided)."
