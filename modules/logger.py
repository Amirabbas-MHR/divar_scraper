import logging
from .configs import *
from time import time


class Logger:
    def __init__(self):
        """
        The logger object to handle logging requests
        """
        self.log_file = LOGS_PATH + str(time()).split()[0] + ".log"

        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                            format=f'%(asctime)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def info(self, message, logger_name):
        """
        logs an info messge
        :param message: message of the log
        :param logger_name: recommended to pass __name__ to track files easier
        :return:
        """
        logging.info(f'{logger_name} >> {message}')
        return
    def warning(self, message, logger_name):
        """
        logs a warning messge
        :param message: message of the log
        :param logger_name: recommended to pass __name__ to track files easier
        :return:
        """
        logging.warning(f'{logger_name} >> {message}')
        return
    def fatal(self, message, logger_name):
        """
        logs a fatal messge
        :param message: message of the log
        :param logger_name: recommended to pass __name__ to track files easier
        :return:
        """
        logging.fatal(f'{logger_name} >> {message}')
        return

