#!/usr/bin/env python
# -*- coding: utf-8 -*-


def poll(response, options, args):
    if args[0] == "begin":
        """
        TODO: remove these return statements, bundle the options into the return, and make a special case in bot.py, or make a global array of response...
        options is an array
        set options[0] to an array that contains the channel it is in, the user that started it, and the timestamp of the poll(that will be set by start), and options[1] to an array that contains the polling options, and options[2] to the status of the poll (none, starting, ongoing, ended).
        """
        if options[2] == "none":
            args[0].pop()
            return begin(response, options, args)  # logic for starting

        elif options[2] == "starting":
            return ["Sorry, a poll is already being set up in this channel. To cancel a poll that has not begun yet, say `!poll end`"]

        elif options[2] == "ongoing":
            return ["Sorry, a poll is already in progress in this channel. Please have the person hosting the poll cancel it, or ask an admin to end it using `!poll end`"]

        elif options[2] == "ended":
            return ["Sorry, a poll is already in progress in this channel. Please have the person hosting the poll cancel it, or ask an admin to end it using `!poll end`"]

    elif args[0] == "start":
        if options[2] == "none":
            return ["Sorry, a poll has not been started on this channel. To start a poll, type `!poll begin`"]

        elif options[2] == "starting":
            return start(response, options, args)

        elif options[2] == "ongoing":
            return ["Sorry, a poll is already in progress in this channel. Please have the person hosting the poll cancel it, or ask an admin to end it using `!poll end`"]

        elif options[2] == "ended":
            return ["Sorry, a poll is already in progress in this channel. Please have the person hosting the poll cancel it, or ask an admin to end it using `!poll end`"]

    elif args[0] == "end":
        return end(response, options, args)

    return


def begin(response, options, args):
    options = []
    pollingOptions = []
    optionString = ""
    x = 0
    for s in range(0, len(args)):
        optionString = optionString + args[s]
        if ";" in args[s]:
            pollingOptions.append(optionString)
            optionString = ""
            x += 1
    print pollingOptions
    message = "Options are: "
    for s in pollingOptions:
        message = message + s + ";\n "
    options[2] = "starting"
    return ["Does this look correct? " + message, "If this is correct, type `!poll start` to begin your poll, or `!poll end` to cancel"]


def start(response, options, args):
    return ["Poll starting"]


def end(response, options, args):
    if options[2] in ["none", "starting"]:
        return ["Poll cancelled"]
    else:
        options[2] = "ended"
        return ["results"]


def results(response, options, args):
    return
