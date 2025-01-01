# test.py
import logging
from utils import daily_logging


logger = logging.getLogger(__name__)
config_func = daily_logging.config_func
config_func(logger)

def my_function():
    logger.info("this is a message from logger")
    x = 1
    try:
        return x / 0
    except ZeroDivisionError:
        logger.exception("ZeroDivisionError")


if __name__ == "__main__":
    my_function()
