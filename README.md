# PantherBot
PantherBot is a WebSocket Application that takes advantage of Slack's RTM and Web API to interact with the channels that it is a part of.

# Using PantherBot
PantherBot currently has a few commands available to use. These are broken up into action commands and logging commands.
All action commands are prefaced with the "!" marker (ie. `!coin`).
Logging commands are prefaced with the "$" marker (ie. `$log`).
Some responses are hard coded to certain phrases (ie. `Hey PantherBot`).

Current list of action commands:
```
!help
!coin
!fortune
!catfact
!pugbomb <number>
!taskme
!flip/!rage flip/!unflip <String of any length containing only ascii characters>
!calendar add ; <Title> ; <Date in format YYYY-MM-DD> ; <Start time in format HH:mm> ; <End time in format HH:mm> ; <Description> ; <Location>
```

Current list of logging commands:
```
$log <true/false> <optional: list of channels>
```

To use these commands, in any channel that PantherBot is both present in and may post, start your message with one of the above commands and fill in the arguments as necessary

PantherBot also responds to a few custom messages as well, currently set to:
```
Hey PantherBot
PantherBot ping
```
As well as messaging them a custom message upon joining the Slack team.

# Installing Dependencies
PantherBot requires several python libraries to function. These can be easily installed with the `setup.bat` or `setup.sh` file.
```
sudo setup.sh
```
`setup.sh` should be run with elevated privileges to ensure dependencies install correctly (this is an issue for most unless you're using a virtualenv).
Likewise, pip may request your permission or a prompt if using the `setup.bat` file. If it fails, try using administrative privileges.

# Setting up PantherBot
PantherBot is currently relatively easy to set up in your Slack team. Follow the instructions below and it'll be up and running in no time!

1. Go to your Slack team settings and set up a bot configuration, be sure to give it some information, including a username! Copy the API token.
2. Set up a System Environment Variable called `SLACK_API_TOKEN`, and set its value to your API token you copied earlier (depends very much on the OS).
3. Depending on your OS, run either `start.bat` for Windows, or run `start.sh` for linux.
4. The bot should become active in the slack team. Invite the bot into the channels you would like it to monitor (using the /invite @username command), and off it goes surveying the world!
5. The bot is set up, if you want to edit anything (like the posting name or icon), edit the bot.py script's `BOT_NAME`, `BOT_ICON_URL`, `TUT_LINK`, `GREETING`, `GOOGLECAL`, `GOOGLECALSECRET`, `ADMIN`. We are looking to add a config file to consolidate this.
