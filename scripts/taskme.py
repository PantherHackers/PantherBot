#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def taskme(response):
	#Sudo code
	arr = []
	#format for this is "[verb, sample output]"
	arr.append(["write a program that prints out the numbers 1 to 100, but when the number is a multiple of 3 it instead prints `foo`, and when it is a multiple of 5 it instead prints `bar`, and when it is a multiple of both it prints `foo bar`.\n", "```1\n2\nfoo\n4\nbar\nfoo\n7\n8\nfoo\nbar\n11\nfoo\n13\n14\nfoobar\n...\n98\nfoo\nbar\n```"])
	arr.append(["do ome test", "Some output"])
	arr.append(["do some other test", "Some other output"])
	n = random.randrange(0, len(arr))
	#Or maybe there's an API
	return arr[n]
