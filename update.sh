#!/bin/bash
cd ..
sudo rm -r PantherBot-old
mv PantherBot PantherBot-old
git clone https://github.com/braxton-mclean/PantherBot.git
mv PantherBot-old/config PantherBot/config
mv PantherBot-old/secrets PantherBot/secrets
mv PantherBot-old/logs PantherBot/logs
pkill python
cd .
cd PantherBot
./start.sh
