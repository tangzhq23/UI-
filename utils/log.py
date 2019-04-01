"""
日志类。通过读取配置文件，定义日志级别、日志文件名、日志格式等。
一般直接把logger import进去
from utils.log import logger
logger.info('test log')
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler  # TimedRotatingFileHandler这个模块是满足文件名按时间自动更换的需求
from 豆瓣.test_douban.utils.config import Config,LOG_PATH

class Logger(object):
    def __init__(self, logger_name="framework"):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)  # 设置日志级别
        c = Config().get('log')
        self.log_file_name = self.log_file_name = c.get('file_name') if c and c.get('file_name') else 'test.log'  # 日志文件
        self.backup_count = c.get('backup') if c and c.get('backup') else 5  # 保留的日志数量
        # 日志输出级别
        self.console_output_level = c.get('console_level') if c and c.get('console_level') else 'WARNING'
        self.file_output_level = c.get('file_level') if c and c.get('file_level') else 'DEBUG'
        '''字符串格式化，%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒、%(name)s Logger的名字
        、%(levelname)s 文本形式的日志级别、%(message)s 用户输出的消息'''
        pattern = c.get('pattern') if c and c.get('pattern') else '%(asctime)s - %(name)s - %(levelname)s - %(message)s' # 日志输出格式
        self.formatter = logging.Formatter(pattern)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
        我们这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
        两个句柄的日志级别不同，在配置文件中可设置。"""
        if not self.logger.handlers:  # 避免重复日志
            # stream: 指定将日志的输出流，可以指定输出到sys.stderr, sys.stdout或者文件，默认输出到sys.stderr，当stream和filename同时指定时，stream被忽略
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Logger().get_logger()
