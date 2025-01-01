1. 创建日志配置模块 (logging_config.py)

创建一个名为 logging_config.py 的文件，用于配置日志记录器。这个模块将包含日志记录器的基本设置，例如日志级别、格式和处理器。

Python
import logging
import os

def setup_logger(log_file_path, log_level=logging.INFO):
    """配置日志记录器。"""

    # 创建日志目录，如果不存在
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建日志记录器
    logger = logging.getLogger(__name__)  # 使用模块名作为 logger 的名字
    logger.setLevel(log_level)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 创建控制台处理器
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 创建文件处理器
    fh = logging.FileHandler(log_file_path, mode='a', encoding='utf-8') # mode='a' for append
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# 示例配置，可以根据需要修改
LOG_FILE = "logs/my_app.log" # 日志文件路径
LOG_LEVEL = logging.DEBUG # 日志级别
logger = setup_logger(LOG_FILE, LOG_LEVEL)

if __name__ == '__main__':
    # 示例用法
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
2. 在你的代码中使用 logger

在你的其他模块中，导入配置好的 logger 并使用它。

Python
# my_module.py
import logging_config # 导入日志配置模块

# 获取 logger。注意使用 __name__ 来获取当前模块的名称
logger = logging_config.logger #直接使用配置模块中定义的logger

def my_function():
    logger.info("This is a message from my_function")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("An exception occurred") # 记录异常的完整堆栈信息

if __name__ == '__main__':
    my_function()
3. 工程结构示例

推荐的工程结构如下：

my_project/
├── main.py       # 主程序入口
├── my_module.py  # 其他模块
└── logging_config.py # 日志配置
└── logs/           # 日志文件夹
    └── my_app.log   # 日志文件
关键改进和解释：

模块化配置: 将日志配置放在单独的 logging_config.py 文件中，使得配置更加清晰和易于维护。其他模块只需要导入这个模块即可使用配置好的 logger。
使用 __name__: 在 logging.getLogger() 中使用 __name__ 是最佳实践。这使得每个模块都有自己的 logger，方便追踪日志信息的来源。
创建日志目录: 代码中添加了创建日志目录的逻辑，避免了因目录不存在而导致的错误。
文件追加模式: 使用 mode='a' 打开日志文件，以追加模式写入，避免每次运行都覆盖之前的日志。
UTF-8 编码: 使用 encoding='utf-8' 确保日志文件可以正确处理各种字符。
异常记录: 使用 logger.exception() 可以记录异常的完整堆栈信息，这对于调试非常有用。
直接使用配置模块中定义的logger: 无需在每个模块中都调用logging.getLogger(__name__)，可以直接使用logging_config.logger，简化了代码。
使用方法：

将 logging_config.py 放在你的项目根目录下。
在需要使用日志的模块中，导入 logging_config 模块并使用 logging_config.logger。
运行你的程序。日志信息将同时输出到控制台和 logs/my_app.log 文件中。
这个方法提供了一个清晰、可维护且易于扩展的日志解决方案，适用于各种规模的 Python 项目。通过调整 LOG_LEVEL 变量，你可以控制记录的日志级别，例如设置为 logging.DEBUG 记录所有信息，或设置为 logging.ERROR 只记录错误和严重错误。
