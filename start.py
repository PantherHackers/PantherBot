import threading, time, logging, os, sys, codecs
from bot import Bot

if __name__ == "__main__":
    print "PantherBot:LOG:Beginning Execution... Setting up"

    # Checks if the system's encoding type is utf-8 and changes it to utf-8 if it isnt (its not on Windows by default)  # noqa: 501
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')

    # Initialize logger functionality to read errors more easily from the terminal
    # This is due to WebSockets requiring outside logging methods 
    logger = logging.getLogger('root')
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.DEBUG)

    # Initializes our primary bot
    # This is the reactive bot known as "PantherBot," and is responsible for all message detection and immediate reactions
    print "PantherBot:LOG:Initializing bot"
    token = os.environ.get('PB_TOKEN')

    # List of all bots running in current process.
    BOT_LIST = []
    react_bot = Bot(token, is_websocket=True, bot_name="PantherBot")
    BOT_LIST.append(react_bot)
    bot_thread = threading.Thread(target=react_bot.WEBSOCKET.run_forever, kwargs={"ping_interval":30, "ping_timeout":10})
    print "PantherBot:LOG:Beginning thread"
    bot_thread.start()

    proactive_bot = Bot(token, is_websocket=False, bot_name="PantherBot")
    while True:
        time.sleep(300)
        for b in BOT_LIST:
            if b.WEBSOCKET != None:
                b.pb_cooldown = True
        proactive_bot.smsg("random", "Today is a good day")
        print "PantherBot:LOG:Proactive still alive"