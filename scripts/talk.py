#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
def talk(response, args=[]):
    cb = ChatBot('PantherBot')
    cb.set_trainer(ChatterBotCorpusTrainer)
    cb.train(
    "chatterbot.corpus.english"
    )
    try:
        return [cb.get_response(" ".join(args)).text]
    except:
        return ["I'm feeling sick... come back later"]