#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleverbot import Cleverbot

def talk(response, args):
    return Cleverbot().ask(" ".join(args))
