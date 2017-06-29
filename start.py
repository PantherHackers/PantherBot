import threading, time, logging, os, sys, codecs

from bot import Bot
from reactbot import ReactBot

import log_handler

if __name__ == "__main__":
    # See here for logging documentation https://docs.python.org/2/howto/logging.html
    
    # Set the name for the logger
    # Add custom log handler to logger
    logger = logging.getLogger('PantherBot')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler.PBLogHandler())

    logger.info("Beginning Execution... Setting up")

    # Checks if the system's encoding type is utf-8 and changes it to utf-8 if it isnt (its not on Windows by default)  # noqa: 501
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')

    # Initializes our primary bot
    # This is the reactive bot known as "PantherBot," and is responsible for all message detection and immediate reactions
    logger.info("Initializing bot")
    token = os.environ.get('PB_TOKEN')

    # List of all bots running in current process.
    BOT_LIST = []
    react_bot = ReactBot(token, bot_name="PantherBot")
    BOT_LIST.append(react_bot)
    bot_thread = threading.Thread(target=react_bot.WEBSOCKET.run_forever, kwargs={"ping_interval":30, "ping_timeout":10})
    logger.info("Beginning thread")
    bot_thread.start()

    proactive_bot = Bot(token, bot_name="PantherBot")
    count_interval = 0

    while True:
        try:
            time.sleep(600)
            count_interval += 1
            for b in BOT_LIST:
                if b.WEBSOCKET != None:
                    b.pb_cooldown = True
            if count_interval == 72:
                proactive_bot.smsg("pantherbot-dev", "Check-in")
                count_interval = 0
            logger.info("Proactive still alive")
        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
            react_bot.close()
            break
