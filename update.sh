#!/bin/bash
sudo rm -r ../PantherBot-old
cp -R ../PantherBot ../PantherBot-old
git pull
pkill -f bot.py
./setup.sh
./start.sh
