#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Created by Harsha Goli
import praw
import re

#pug bombs the chat and destroys this poor bot's soul
def pugbomb(response, args):
    #gets the number
    num = int(args[0])
    if num > 10:
        num = 10

    reddit = praw.Reddit(client_id='aGpQJujCarDHWA',
                        client_secret='fkA9lp0NDx23B_qdFezTeGyGKu8',
                        user_agent='my user agent',
                        password='PHGSU2017',
                        username='Panther_Bot')
    
    pug_urls=[]
    for submission in reddit.subreddit('pugs').hot(limit=num):
        url = submission.url
        if re.search(r'(imgur)', submission.url, flags = 0) != None and re.search(r'(\.jpg|\.png|\.jpeg)', submission.url, flags = 0) == None:
            url+=('.jpg')
        
        pug_urls.append(url)

    pug_urls.append("""
        `Having issues? Try Preferences > Messages > 'Even if theyre larger than 2MB'`
        """)  
    return pug_urls
