#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Template: Include this so this file supports unicode characters in it.

#Name your file with the title of your method, both of which should be all lowercase.
def helloworld(response, args=None): #response is always given to you, good for checking on user info or something unique to a message object, args is optional, or if your function may not take args, set it to None or [] depending on your needs
	#do your logic here
	message = "Hello World:"
	if args != None:
		for x in range(0, len(args)): #For loop that goes from the second element of args (to skip the command) to the last element
			message += " " + args[x] #adds a space and the next argument from the message call

	#Always return a list of strings (can be a list containing only one string) that will be be all the messages sent by PantherBot in that order
	#Example, if I have ["Hello", "World"] PantherBot would send two messages, the first being "Hello," the second "World".
	#Likewise, ["Hello World"] will have PB send one message, being "Hello World".
	#Sometimes your logic may be working with an array of strings already, so its fine to just return that (dont return an array containing arrays, plz.)
	return [message]
