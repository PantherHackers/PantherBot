#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import sys
from response import Response

def run(response, args=[]):
    response_obj = Response(sys.modules[__name__])
    cb = ChatBot('PantherBot')
    cb.set_trainer(ChatterBotCorpusTrainer)
    cb.train(
    "chatterbot.corpus.english"
    )
    try:
        response_obj.messages_to_send.append(cb.get_response(" ".join(args)).text)
    except:
        response_obj.messages_to_send.append("I'm feeling sick... come back later")
    return response_obj

def return_alias():
    alias_list = ["talk"]
    return alias_list

def is_admin_command():
    return False