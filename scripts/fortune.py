#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2


# returns a random "fortune"
def fortune(response):
    try:
        # get fortune
        fortune = urllib2.urlopen("http://www.fortunefortoday.com/getfortuneonly.php").read()  # noqa: 501
    except:
        fortune = "Unable to reach fortune telling api"
        print "PantherBot:Log:Fortune:Error in receiving fortune"

    # make api call
    return [fortune]
