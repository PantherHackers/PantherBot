#!/bin/bash
#only use if you used an older version of the PantherBot distribution on linux, in which case your dependancies are broken and get a websocket import error from SlackCLient
pip uninstall websocket
pip uninstall websocket-client
pip install websocket-client
