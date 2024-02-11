from pandas import DataFrame as Df
from .configs import RECORDS_PATH
from dataclasses import asdict
from time import time
from .configs import *
import logging as log


class Recorder:
    def __init__(self, logger, file_name: str, tank_size: int = 10):
        self.file_path = RECORDS_PATH + file_name
        self.tank_size = tank_size
        self.tank = []
        self.logger = logger


    def __file_exsits(self) -> bool:
        # TODO write this shit
        pass

    def flush(self):
        if len(self.tank) > 0:
            print(f'\n -> flushing {len(self.tank)} records to {self.file_path}.\n')
            self.logger.info(f"{len(self.tank)} posts flushed to {self.file_path}", __name__)
            table = Df(self.tank)
            # Set header to False if the file already exists
            table.to_csv(self.file_path, mode='a', index=False, header=not self.__file_exsits())
            self.tank = []

    def record(self, post):
        record = {**asdict(post), 'record_time': time()}  # adding the record_time to the post dict
        self.logger.info(f"post <{post.token}> added to tank", __name__)
        self.tank.append(record)
        if len(self.tank) >= self.tank_size:
            self.flush()
