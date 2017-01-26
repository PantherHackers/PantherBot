#!/usr/bin/env python
# -*- coding: utf-8 -*-


# help script that details the list of commands
def help(response):
    text = "PantherBot works by prefacing commands with \"!\"\n"
    text += "Commands:\n"
    text += "```!help\n"
    text += "!coin\n"
    text += "!helloworld\n"
    text += "!version\n"
    text += "!fortune\n"
    text += "!flip <Optional:String>\n"
    text += "!unflip <Optional:String>\n"
    text += "!rage <Optional:String>\n"
    text += "!catfact\n"
    text += "!pugbomb <int>\n"
    text += "!taskme\n"
    text += "!talk <String>\n"
    text += "\"Hey PantherBot\"```\n"
    text += "Try saying `Hey PantherBot` or `!coin`"

    motext = "Admins are able to use admin commands prefaced with \"$\"\n"
    motext += "```$calendar add ; <Title> ; <Date in format YYYY-MM-DD> ; <Start time in format HH:mm> ; <End time in format HH:mm> ; <Description> ; <Location>\n"  # noqa: 501
    motext += "$admin <reconnect/update>\n"
    motext += "$log <true/false> <channels>```\n"
    motext += "Got suggestions for PantherBot? Fill out our typeform to leave your ideas! https://goo.gl/rEb0B7"  # noqa: 501
    return [text, motext]
