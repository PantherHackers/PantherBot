# PantherBot
PantherBot is a WebSocket Application that takes advantage of Slack's RTM API to interact with the channels that it is a part of.

# Using PantherBot
PantherBot currently has a few commands available to use. These are broken up into action commands and logging commands.
All action commands are prefaced with the "!" marker (ie. `!coin`).
Logging commands are prefaced with the "$" marker (ie. `$log`).

Current list of action commands:
```
!help
!coin
!fortune
!catfact
!pugbomb <number>
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

# Running PantherBot
PantherBot is currently relatively easy to set up in your Slack team. Follow the instructions below and it'll be up and running in no time!

1. Go to your Slack team settings and set up a bot configuration, be sure to give it some information, including a username! Copy the API token.
2. Set up a System Environment Variable called `SLACK_API_TOKEN`, and set its value to your API token you copied earlier.
3. Start the bot.py script. The included start.bat script is good enough on Windows setups. If you're running Linux I'm sure it won't be much harder.
4. The bot should become active in the slack team. Invite the bot into the channels you would like it to monitor (using the /invite @username command), and off it goes surveying the world!
5. The bot is set up, if you want to edit anything (like the posting name or icon), edit the bot.py script's `BOT_NAME`, `BOT_ICON_URL`, `TUT_LINK`, `GREETING`, `GOOGLECAL`, `GOOGLECALSECRET`, `ADMIN`.
