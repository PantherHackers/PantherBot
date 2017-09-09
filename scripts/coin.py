#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


# flips a coin
def coin(response):
    l = ["Heads", "Tails"]
    m = random.randrange(0, 2)
    return [l[m]]
