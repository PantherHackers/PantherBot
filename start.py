import threading, time, logging, os, sys
from bot import Bot

if __name__ == "__main__":
    print "PantherBot:LOG:Beginning Execution... Setting up"

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

    BOT_LIST = []
    bot = Bot(token, is_websocket=True, bot_name="PantherBot")
    BOT_LIST.append(bot)
    bot_thread = threading.Thread(target=bot.WEBSOCKET.run_forever, kwargs={"ping_interval":30, "ping_timeout":10})
    print "PantherBot:LOG:Beginning thread"
    bot_thread.start()
    while True:
        time.sleep(300)
        for b in BOT_LIST:
            if b.WEBSOCKET != None:
                b.pb_cooldown = True
        print "PantherBot:LOG:Proactive still alive"