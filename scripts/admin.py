#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess, platform, sys, os

def admin(response, args, sc, rmsg):
	if args[0].lower() == "update":
		updateBot(response, rmsg)
	if args[0].lower() == "reconnect":
		reconnectBot(response, rmsg)

#Update function for PantherBot so it clones latest master, replaces directories, and restarts. Currently not functional
def updateBot(response, rmsg):
	print "PantherBot:LOG:Updating..."
	rmsg(response, ["Updating..."])
	script_dir = os.path.dirname(os.path.dirname(__file__))
	proc = subprocess.Popen("./update.sh", cwd=script_dir, shell=True)

#does not conserve memory, the other process is left open
def reconnectBot(response, rmsg):
	p = platform.system()
	rmsg(response, ["Rebooting..."])
	script_dir = os.path.dirname(os.path.dirname(__file__))
	if p == "Windows":
		proc = subprocess.Popen("reconnect.bat", cwd=script_dir, shell=True)
	elif p == "Linux":
		proc = subprocess.Popen("sh reconnect.sh", cwd=script_dir, shell=True)
