#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template: Include this so this file supports unicode characters in it.

# Always import these two pieces at least
import sys
from response import Response

# Import these so that you can use the logger functions
# so that you can log things
import logging
import log_handler

# If you need to print something that will be used for official logging purposes
# use this logger class using the custom handler PBHandler from the log_handler class
logger = logging.getLogger('PantherBot')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler.PBLogHandler())

# Name your file with the title of your method, both of which should be all lowercase.
def helloworld(response, args=None):  # response is always given to you, good for checking on user info or something unique to a message object, args is optional, or if your function may not take args, set it to None or [] depending on your needs
    # This is your response_obj, it should be returned at the end of your script (or logic that calls for it to end early)
    # See response.py at the root of the project directory to see how it works in more depth
    response_obj = Response(sys.modules[__name__])
    # do your logic here
    message = "Hello World:"
    if args is not None:
        for x in range(0, len(args)):  # For loop that goes from the second element of args (to skip the command) to the last element
            message += " " + args[x]  # adds a space and the next argument from the message call

    # You should have all messages you wish sent to chat in the `messages_to_send` field. 
    # It is by default an empty array, so you may append messages to it easily.
    response_obj.messages_to_send.append(message)

    # Your script may run into user error! In such a case, you can define the `status_code` field of response_obj to something not 0
    # If it is not 0, the scripts `error_cleanup` method will be called after the current method finishes.
    possible_error = 0
    if possible_error is not 0:
        response_obj.status_code = -1
    return response_obj

# Called before the script's main function (ie `helloworld()` above) to describe the purpose of the function
# If admins are the only ones allowed to call this script's functionality, this should return True
def is_admin_command():
    return False

# Called after the main function of the script should it return a status code that is not 0
def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("AHHHH! FIRE! Explain your error here, especially if it is user error")

        # You can log an error this way
        logger.error("[Hello World] Error: FIRE!")
    else:
        # If for some reason your script returned a status_code of something you weren't expecting, this is here to catch that
        response_obj.messages_to_send.append("An unknown error occured. Error code: " + error_code)

        # You can log an error here too
        logger.error("[Hello World] Error: " + error_code)
    return response_obj