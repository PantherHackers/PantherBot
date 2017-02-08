#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Created by Harsha Goli
import praw

#pug bombs the chat and destroys this poor bot's soul
def pugbomb(response, args):
    
	#gets the number
	#num = [int(s) for s in response["text"].split() if s.isdigit()]
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
        pug_urls.append(submission.url)
	return pug_urls
