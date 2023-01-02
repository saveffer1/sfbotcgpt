from src import bot
import sys

def check_verion() -> None:
    import pkg_resources
    import src.log

    # init loggger
    logger = src.log.setup_logger(__name__)

if __name__ == '__main__': 
    check_verion()
    bot.run_discord_bot()
