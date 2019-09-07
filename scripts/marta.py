#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
import requests
import json
from response import Response
from marta.api import get_buses, get_trains
from collections import defaultdict

from pb_logging import PBLogger
logger = PBLogger("MARTA")

stations = {
    "AIRPORT STATION": ['airport','hartsfield','hartsfield-jackson'],
    "ARTS CENTER STATION": ['arts center'],
    "ASHBY STATION": ['ashby'],
    "AVONDALE STATION": ['avondale'],
    "BANKHEAD STATION": ['bankhead'],
    "BROOKHAVEN STATION": ['brookhaven'],
    "BUCKHEAD STATION": ['buckhead'],
    "CHAMBLEE STATION": ['chamblee'],
    "CIVIC CENTER STATION": ['civic center'],
    "COLLEGE PARK STATION": ['college park'],
    "DECATUR STATION": ['decatur'],
    "OMNI DOME STATION": ['omni dome'],
    "DORAVILLE STATION": ['doraville'],
    "DUNWOODY STATION": ['dunwoody'],
    "EAST LAKE STATION": ['east lake'],
    "EAST POINT STATION": ['east point'],
    "EDGEWOOD CANDLER PARK STATION": ['edgewood','candler park'],
    "FIVE POINTS STATION": ['five points','5 points'],
    "GARNETT STATION": ['garnett'],
    "GEORGIA STATE STATION": ['georgia state','gsu','school'],
    "HAMILTON E HOLMES STATION": ['hamilton e holmes','h.e. holmes','he holmes'],
    "INDIAN CREEK STATION": ['indian creek'],
    "INMAN PARK STATION": ['inman','inman park'],
    "KENSINGTON STATION": ['kensington'],
    "KING MEMORIAL STATION": ['king memorial','mlk'],
    "LAKEWOOD STATION": ['lakewood'],
    "LENOX STATION": ['lenox'],
    "LINDBERGH STATION": ['lindbergh'],
    "MEDICAL CENTER STATION": ['medical center'],
    "MIDTOWN STATION": ['midtown'],
    "NORTH AVE STATION": ['north ave','north avenue','gt','georgia tech', 'tech'],
    "NORTH SPRINGS STATION": ['north springs'],
    "OAKLAND CITY STATION": ['oakland','oakland city'],
    "PEACHTREE CENTER STATION": ['peachtree center'],
    "SANDY SPRINGS STATION": ['sandy springs'],
    "VINE CITY STATION": ['vine city'],
    "WEST END STATION": ['west end'],
    "WEST LAKE STATION": ['west lake']
}

# flips a coin
def run(response, station=None, line=None, direction=None):
    response_obj = Response(sys.modules[__name__])
    found=False
    stationName = "GEORGIA STATE STATION"
    if station != None: # Default to Georgia State Station if not specified
        stationName = str(station)
    for s in stations:
        if stationName.upper() == s or stationName.lower() in stations[s][0]:
            stationName = s
            found=True
            break
    if not found:
        response_obj.messages_to_send.append("Sorry, I don't know that station.")
        logger.info("Sorry, I don't know that station.")
        return response_obj
    else:
        trains = get_trains(station=stationName)
        if trains:
            if line is not None and line.lower() in ['g','r','b','gold','red','green','blue','y','yellow','o','orange'] and direction is not None and direction.lower() in ['n','s','e','w','north','south','east','west','northbound','southbound','eastbound','westbound']:
                if line.lower().startswith('r'):
                    line = 'RED'
                elif line.lower().startswith('y') or line.lower().startswith('o') or line.lower().startswith('go'):
                    line = 'GOLD'
                elif line.lower().startswith('b'):
                    line = 'BLUE'
                elif line.lower().startswith('g'):
                    line = 'GREEN'
                if direction.lower().startswith('n'):
                    direction = 'N'
                elif direction.lower().startswith('s'):
                    direction = 'S'
                elif direction.lower().startswith('e'):
                    direction = 'E'
                elif direction.lower().startswith('w'):
                    direction = 'W'
            else:
                line = None
                direction = None
            final_trains = []
            if line:
                for t in trains:
                    if t.line == line and t.direction == direction:
                        final_trains.append(t)
            else:
                for t in trains:
                    final_trains.append(t)
            if final_trains:
                final_message = ""
                attach = ("attachments:": []}
                colors = {'Red':"#FF0000",'Gold':"#FFD700",'Blue':"#0000FF",'Green':"#3CB371"}
                for t in final_trains:
                    #final_message = final_message +  t.line.capitalize() + " line train to " + t.destination + " (" + t.direction + "): " + ("Arriving in " + t.waiting_time if t.waiting_time[0].isdigit() else t.waiting_time) + "\n"
                    message = t.line.capitalize() + " line train to " + t.destination + " (" + t.direction + "): " + ("Arriving in " + t.waiting_time if t.waiting_time[0].isdigit() else t.waiting_time)
                    attach['attachments'].append({'fallback': message, 'color': colors[t.line.capitalize()], 'text': message})
                #await ctx.send(final_message)
                response_obj.messages_to_send.append(attach)
                logger.info("Returning some MARTA data...")
                return response_obj
            else:
                #await ctx.send("No trains in the near future.")
                response_obj.messages_to_send.append("No trains arriving for that route.")
                logger.info("No trains arriving for that route.")
                return response_obj
        else:
            #print("No trains near that station.")
            response_obj.messages_to_send.append("No trains near that station.")
            logger.info("No trains near that station.")
            return response_obj

def return_alias():
    alias_list = ["marta"]
    return alias_list

def is_admin_command():
    return False

def help_preview():
    return "!coin"

def help_text():
    return "Flips a coin and returns the result... Sometimes you wonder if people even read these. Heads they don't."
