"""API key-qouta manager.

:Author: Fadwa Maatug
"""
import json, time
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler

from nordlys.config import LOGGING_PATH, Api_Log_Path


class API_Manager(object):
    def __init__(self, Api_Log_Path, logging_path):
        self.api_path = "{0}/api_keys.json".format(Api_Log_Path)  # holds API key-qouta file path
        self.count = 0  # hold the index of the last line in log file
        self.key_dict = dict()
        date = time.strftime("%Y-%m-%d")
        self.log_file = "{0}/api/{1}.log".format(logging_path, date)  # holds the last log file path
        with open(self.api_path) as json_file:
            self.api_file = json.load(json_file)  # loading the API key-qouta file

    def key_validate(self, x):  # fuction to validate the key, it can be change depending on the key generator
        if (len(x) < 6):
            return True

    def func_manager(self):
        with open(self.log_file) as wwwlog:  # loading the log file
            data = wwwlog.readlines()[self.count:]
        key_column = [line.split("key=")[1].strip() for line in data if line.find("key=") != -1]  # extract the key
        key_column = np.array([x for x in key_column if self.key_validate(x) != True])  # check the key validation
        uniq_keys, key_count = np.unique(key_column, return_counts=True)  # count the keys
        self.keys_dict = dict(zip(uniq_keys, key_count))
        for key, value in self.keys_dict.items():
            self.api_file.get(key)['qouta'] += int(value)

    def line_count(self):  # update the index of the last line in log file
        with open(self.log_file) as wwwlog:
            self.count = len(wwwlog.readlines())
        return

    def func_print(self):  # update API key-qouat file
        with open(self.api_path, "w") as write_file:
            json.dump(self.api_file, write_file, indent=4)


def worker():
    api_manager.func_manager()
    api_manager.line_count()
    api_manager.func_print()


if __name__ == "__main__":
    api_manager = API_Manager(Api_Log_Path, LOGGING_PATH)
    try:
        scheduler = BlockingScheduler()
        scheduler.add_job(worker, 'interval', minutes=15)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
