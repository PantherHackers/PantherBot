#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleverbot import Cleverbot

def talk(response, args=[]):
	r = ""
	for s in args:
		r = s + " "
	return [Cleverbot().ask(r)]
