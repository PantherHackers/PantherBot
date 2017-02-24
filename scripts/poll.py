#!/usr/bin/env python
# -*- coding: utf-8 -*-

STARTING_MESSAGE = "Sorry, a poll is already being set up in this channel. To cancel a poll that has not begun yet, say `!poll end`"
BUSY_MESSAGE = "Sorry, a poll is already in progress in this channel. Please have the person hosting the poll cancel it, or ask an admin to end it using `!poll end`"

def poll(response, options, sc, args):
    if args[0] == "begin":
        """
        set options[0] to the timestamp of the poll(that will be set by start's posted message (see bot.py)), and options[1] to an array that contains the polling options, and options[2] to the status of the poll (none, starting, ongoing, ended).
        options = ["timestamp",[polling_options],"status"]
        """
        if options[2] == "none":
            args.pop(0)  # get rid of the "begin" element
            return begin(response, options, args)  # logic for starting

        elif options[2] == "starting":
            return [STARTING_MESSAGE]

        elif options[2] == "ongoing":
            return [BUSY_MESSAGE]

        elif options[2] == "ended":
            return [BUSY_MESSAGE]

    elif args[0] == "start":
        if options[2] == "none":
            return ["Sorry, a poll has not been started on this channel. To start a poll, type `!poll begin`"]

        elif options[2] == "starting":
            return start(response, options, args)

        elif options[2] == "ongoing":
            return [BUSY_MESSAGE]

        elif options[2] == "ended":
            return [BUSY_MESSAGE]

    elif args[0] == "end":
        return end(response, options, sc, args)
    elif args[0] == "results":
        return [results(response,options,sc,args)]
    return ["You seemed to have used this method incorrectly... see !help to see how to use it"]


def begin(response, options, args):
    op = []
    polling_options = []
    option_string = ""
    for arg in args:
        option_string = option_string + arg + " "
        if ";" in arg:
            polling_options.append(option_string[:-2])
            option_string = ""
    if len(polling_options) > 10:
        return ["Sorry, I'm currently capped at ten options right now, what kind of poll are you looking to do?"]
    message = "Options are:\n"
    message = message + '\n'.join(polling_options)
    options[1] = polling_options
    options[2] = "starting"
    return ["Does this look correct?\n" + message, "If this is correct, type `!poll start` to begin your poll, or `!poll end` to cancel"]


def start(response, options, args):
    arr_of_emojis = [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:",":keycap_ten:"]
    ops = options[1]
    options[1] = dict()
    options[2] = "ongoing"
    message = ""
    for index, op in enumerate(ops):
        options[1][op] = arr_of_emojis[index]
    for key in options[1]:
        message = message + key + ": " + options[1][key] + "\n"
    return ["Poll starting", "POLL_BEGIN " + response["channel"] + ";\n" + message]


def end(response, options, sc, args):
    if options[2] in ["none", "starting"]:
        options[2] = "none"
        return ["Poll cancelled"]

    elif options[2] == "ongoing":
        options[2] = "none"
        return ["Poll concluded", results(response,options,sc,args)]

    else:
        options[2] = "none"
        return [results(response,options,sc,args)]


def results(response, options, sc, args):
    r = sc.api_call(
            "reactions.get",
            channel=response["channel"],
            timestamp=options[0],
            full="true"
        )

    reac_dict = dict()
    winner = ""
    count = 0
    for reaction in r["message"]["reactions"]:
        reac_dict[reaction["name"]] = reaction["count"] - 1
        # if int(reaction["count"]) > count:
        #     winner = reaction["name"]
        #     count = int(reaction["count"])

    message = "Results:\n"
    for key in options[1]:
        message = message + key + ": " + str(reac_dict[options[1][key].strip(":")]) + "\n"
        
    # message += "\nThe Winner is:\n:tada:" + winner + ":tada:"
    return message
