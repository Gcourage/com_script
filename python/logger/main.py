import logging
from utils import daily_logging
import test

# 在 main.py 中取得 logger
logger = logging.getLogger(__name__)
config_func = daily_logging.config_func
config_func(logger)

logger.info("This is a message from main.py")
test.my_function()
