#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleverbot import Cleverbot

def talk(response, args=[]):
	r = ""
	for s in args:
		r = r + s + " "
	print r
	return [Cleverbot().ask(r)]
