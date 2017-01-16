#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleverbot import Cleverbot

def talk(talk):
    return Cleverbot().ask(" ".join(talk))
