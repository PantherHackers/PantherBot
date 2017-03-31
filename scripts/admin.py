#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess, platform, os 
import sys
from response import Response


def admin(response, args, sc, rmsg):
    if args[0].lower() == "update":
        updateBot(response, rmsg)


# Update function for PantherBot so it clones latest master, replaces directories, and restarts. Currently not functional  # noqa: 501
def updateBot(response, rmsg):
    print "PantherBot:LOG:Updating..."
    rmsg(response, ["Updating..."])
    script_dir = os.path.dirname(os.path.dirname(__file__))
    proc = subprocess.Popen("./update.sh", cwd=script_dir, shell=True)