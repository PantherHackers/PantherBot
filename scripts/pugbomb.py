#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw


def pugbomb(response, args):
    #gets the number
    try:
        num = round(int(args[0]))
    except:
        return "`Please enter a number`"

    if num > 10:
        num = 10
    elif num <= 0:
        return "`Can only show one or more pugs`"

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
    return pug_urls
