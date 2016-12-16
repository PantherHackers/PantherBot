#!/usr/bin/env python
# -*- coding: utf-8 -*-

#help script that details the list of commands
def help(response):
	text = "PantherBot works by prefacing commands with \"!\"\n"
	text += "Commands:\n"
	text += "```!help\n"
	text += "!coin\n"
	text += "!fortune\n"
	text += "!flip <String>\n"
	text += "!rage flip <String>\n"
	text += "!catfact\n"
	text += "!pugbomb <int>\n"
	text += "\"Hey PantherBot\"```\n"
	text += "Try saying `Hey PantherBot` or `!coin`"
	return text
	