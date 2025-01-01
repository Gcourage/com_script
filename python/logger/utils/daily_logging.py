import logging
import os

def setup_logger(log_file_path, log_level=logging.INFO):
    """配置日志记录器。"""

    # 创建日志目录，如果不存在
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 创建控制台处理器
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    fh = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    fh.setFormatter(formatter)

    def config_logger(logger):
        logger.setLevel(log_level)
        logger.addHandler(ch)
        logger.addHandler(fh)

    return config_logger

# 示例配置，可以根据需要修改
LOG_FILE = "logs/my_app.log" # 日志文件路径
LOG_LEVEL = logging.DEBUG # 日志级别
config_func = setup_logger(LOG_FILE, LOG_LEVEL)