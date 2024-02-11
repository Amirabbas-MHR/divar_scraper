import logging
from .configs import *
from time import time


class Logger:
    def __init__(self):
        self.log_file = LOGS_PATH + str(time()).split()[0] + ".log"

        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                            format=f'%(asctime)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def info(self, message, logger_name):
        logging.info(f'{logger_name} >> {message}')
        return
    def warning(self, message, logger_name):
        logging.warning(f'{logger_name} >> {message}')
        return
    def fatal(self, message, logger_name):
        logging.fatal(f'{logger_name} >> {message}')
        return

