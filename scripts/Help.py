#!/usr/bin/env python
# -*- coding: utf-8 -*-

#help script that details the list of commands
def help(response):
	print "ey"
	text = "PantherBot works by prefacing commands with \"!\"\n"
	text += "Commands:\n"
	text += "```!help\n"
	text += "!coin\n"
	text += "!helloworld\n"
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
	print "howdy"

	motext = "Admins are able to use admin commands prefaced with \"$\"\n"
	motext += "```$calendar add ; <Title> ; <Date in format YYYY-MM-DD> ; <Start time in format HH:mm> ; <End time in format HH:mm> ; <Description> ; <Location>\n"
	motext += "$admin <reconnect/update>\n"
	motext += "$log <true/false> <channels>```"
	print "boi"
	return [text, motext]
