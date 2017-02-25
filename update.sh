#!/bin/bash
rm -rf ../PantherBot-old
cp -R ../PantherBot ../PantherBot-old
git pull
pkill -f bot.py
./setup.sh
./start.sh
