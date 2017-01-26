#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


# enables logging of messages on a channel/channels, storing the logs sorted by channel by day in the format "channelID Y-M-D"  # noqa: 501
def log(response, args, sc, rmsg):
    LOG = False
    LOGC = []

    # Finds log.txt, opens it, and assigns values based on its contents
    filename = "config/log.txt"
    script_dir = os.path.dirname(os.path.dirname(__file__))
    fullDir = os.path.join(script_dir, filename)
    target = open(fullDir, "r")
    if target.readline().strip('\n') == "True":
        LOG = True
    LOGC = [line.rstrip('\n') for line in target]
    target.close()

    # If the first argument is true,
    if "true" == args[0].lower():
        LOG = True
        if len(args) > 1:
            print "PantherBot:LOG:List of channels to log gathered"
            # obtains list of public channels PB is in
            pub_channels = sc.api_call("channels.list", exclude_archived=1)
            # obtains list of private channels PB is in
            pri_channels = sc.api_call("groups.list", exclude_archived=1)
            # Goes through the arguments after true
            print "PantherBot:LOG:Parsing list of channels to log"
            for w in range(1, len(args)):
                # goes through the list of public channels, if found by name, its ID is added to the list of channels to go monitor
                for channel in pub_channels["channels"]:
                    if channel["name"].lower() == args[w].lower():
                        LOGC.append(str(channel["id"]))
                        rmsg(response, [channel["name"] + " added to list of channels to log"])
                # Same as above
                for channel in pri_channels["groups"]:
                    if channel["name"].lower() == args[w].lower():
                        LOGC.append(str(channel["id"]))
                        rmsg(response, [channel["name"] + " added to the list of private channels to log"])
        else:
            print "PantherBot:LOG:No Channels listed to log, logging channel $log was called in"
            rmsg(response, ["No channels listed to log, defaulting to this channel."])
            LOGC.append(str(response["channel"]))
        target = open(fullDir, "w+")
        target.write("True\n")
        for channel in LOGC:
            target.write(channel + "\n")
        target.close()
        return
    elif "false" == args[0].lower():
        print "PantherBot:LOG:Disabling logging"
        target = open(fullDir, "w+")
        target.write("False")
        rmsg(response, ["Logging disabled."])
        return
