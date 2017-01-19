#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleverbot import Cleverbot
import pdb

def talk(response, args=[]):
	r = ""
	for s in args:
		r = r + s + " "
	r = r.encode(encoding='utf-8')
	return [Cleverbot().ask(r)]
