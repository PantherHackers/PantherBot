#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from response import Response

from pb_logging import PBLogger
from scripts import commands
logger = PBLogger("Help")

# help script that details the list of commands
def run(response, args=None):
    response_obj = Response(sys.modules[__name__])

    #Default call to !help
    if args is None:
        commands_help_text = "PantherBot works by prefacing commands with \"!\"\nCommands:\n```"
        commands_help_text += "!version"

        list_of_used_commands = []
        for value in commands.values():
            if value not in list_of_used_commands:
                list_of_used_commands.append(value)
                get_help_preview = getattr(value, "help_preview")
                commands_help_text += get_help_preview() + "\n"
        commands_help_text += "```\nAdmins can use `$` commands\n"
        commands_help_text += "Got suggestions for PantherBot? Fill out our typeform to leave your ideas! https://goo.gl/rEb0B7"
        
        response_obj.messages_to_send.append(commands_help_text)
        logger.info("Help response")
        return response_obj
    elif len(args) is 1:
        command_help_text = "Help info for command: `" + args[0] + "`\n"
        try:
            get_command_help = getattr(commands[args[0]], "help_text")
            command_help_text += get_command_help()
        except:
            response_obj.status_code = -1
            return response_obj
        response_obj.messages_to_send.append(command_help_text)
        return response_obj
    elif len(args) > 1:
        response_obj.status_code = -2
        return response_obj


def error_cleanup(error_code):
    response_obj = Response(sys.modules[__name__])
    if error_code is -1:
        response_obj.messages_to_send.append("That is an invalid command name or alias for said command. Please use `!help` for the full list of commands.")
        logger.error("Error: User requested unavailable command")
    elif error_code is -2:
        response_obj.messages_to_send.append("Multiple commands are not supported.")
        logger.error("Error: User requested multiple commands")
    else:
        response_obj.messages_to_send.append("An unknown error occured. Error code: " + error_code)
        logger.error("Error: Unknown error code" + error_code)
    return response_obj

def return_alias():
    alias_list = ["help", "h"]
    return alias_list

def is_admin_command():
    return False

def help_preview():
    return "!help <Optional:Command>"

def help_text():
    return "Returns the list of commands PantherBot can do, as well as specific command help. You're using the command so you kind of know how it works, but did you know that PantherBot has been rewritten about 4 times now?"