#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import sys
from response import Response

def run(response, pb_cooldown, args):
    response_obj = Response(sys.modules[__name__])
    if pb_cooldown is False:
        response_obj.messages_to_send.append("Sorry, pugbomb is on cooldown.")
        return response_obj

    try:
        num = round(int(args[0]))
    except:
        # not a number
        response_obj.status_code = -1
        return response_obj

    if num > 10:
        num = 10
    elif num <= 0:
        # not more than 0
        response_obj.status_code = -2

    reddit = praw.Reddit(client_id='aGpQJujCarDHWA',
                        client_secret='fkA9lp0NDx23B_qdFezTeGyGKu8',
                        user_agent='my user agent',
                        password='PHGSU2017',
                        username='Panther_Bot')
    
    pug_urls=[]
    for submission in reddit.subreddit('pugs').hot(limit=num):
        if 'imgur' in submission.url and not '.jpg' in submission.url and not '.png' in submission.url and not '.jpeg' in submission.url:
            submission.url+=('.jpg')
        
        pug_urls.append(submission.url)

    pug_urls.append("""
        `Having issues viewing pugs? Try Preferences > Messages > 'Even if theyre larger than 2MB'`
        """)  
    response_obj.messages_to_send = pug_urls
    response_obj.special_condition = True
    return response_obj

def return_alias():
    alias_list = ["pugbomb"]
    return alias_list

def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("Sorry, you didn't enter a number!")
    elif error_code is -2:
        response_obj.messages_to_send.append("Sorry, I can't give you negative pugs.")
    else:
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
    return "!pugbomb"

def help_text():
    return "RETURNS YOU BEAUTIFUL REDDIT PUGS. Pugs are my favorite."