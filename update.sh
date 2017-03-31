#!/bin/bash
rm -rf ../PantherBot-old
cp -R ../PantherBot ../PantherBot-old
git pull
pkill -f start.py
./setup.sh
./start.sh
