#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import sys
from response import Response

def pugbomb(response, args):
    response_obj = Response(sys.modules[__name__])
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
    return response_obj

def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("Sorry, you didn't enter a number!")
    else:
        response_obj.messages_to_send.append("An unknown error occured. Error code: " + error_code)
    response_obj.special_condition = True
    return response_obj

def set_cooldown(bot):
    bot.pb_cooldown = True

def special_condition(bot):
    set_cooldown(bot)