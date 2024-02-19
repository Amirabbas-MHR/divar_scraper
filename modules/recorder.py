from pandas import DataFrame as Df
from .configs import RECORDS_PATH
from dataclasses import asdict
from time import time
from .configs import *
from os.path import exists


class Recorder:
    def __init__(self, logger, file_name: str, tank_size: int = 10):
        """
        The recorder object the catch and save recroded data extracted from posts

        :param logger: the logger object to trigger logging
        :param file_name: file_name to record the extracted data
        :param tank_size: maximum number of objects held in the memory before flushing it to disk (saving as a file)
        """
        self.file_path = RECORDS_PATH + file_name
        self.tank_size = tank_size
        self.tank = []
        self.logger = logger

    def __file_exsits(self) -> bool:
        return exists(self.file_path)

    def flush(self) -> None:
        """
        Flushes the tank of stores data dictionaries held in memory to self.filename
        :return: None
        """
        if len(self.tank) > 0:
            print(f'\n -> flushing {len(self.tank)} records to {self.file_path}.\n')
            self.logger.info(f"{len(self.tank)} posts flushed to {self.file_path}", __name__)
            table = Df(self.tank)
            # Set header to False if the file already exists
            table.to_csv(self.file_path, mode='a', index=False, header=not self.__file_exsits())
            self.tank = []

    def record(self, post):
        """
        Records a single post to self.tank
        :param post: Post object, to be used to record its data
        :return: None
        """
        record = {**asdict(post), 'record_time': str(time()).split(".")[0]}  # adding the record_time to the post dict
        del record['logger']

        self.logger.info(f"post <{post.token}> added to tank", __name__)
        self.tank.append(record)
        if len(self.tank) >= self.tank_size:
            self.flush()
