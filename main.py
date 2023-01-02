from src import bot
import sys

def check_verion() -> None:
    import pkg_resources
    import src.log

    # init loggger
    logger = src.log.setup_logger(__name__)

if __name__ == '__main__': 
    check_verion()
    print("Watchdog start:")
    while True: # run forever
        print("Watchdog: process started")  # program started message
        exec(open("./watchdog.py").read())   # run the program
        print("Watchdog: process finished") # program stopped message
    print("Watchdog end:") # the watchdog is now finishing
    bot.run_discord_bot()
