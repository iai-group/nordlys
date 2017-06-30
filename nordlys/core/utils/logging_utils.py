"""
Logging Utils
=============

Utility methods for logging.

:Author: Heng Ding
"""
import logging, time


class RequestHandler(object):
    """Handler for elastic request"""
    def __init__(self, logging_path):
        self.fh = self._init_handler(logging_path)

    def _init_handler(self, logging_path):
        """Create log file base on logging time setting"""
        date = time.strftime("%Y-%m-%d")  # get current date
        log_file = "{0}/api/{1}.log".format(logging_path, date)
        fh = logging.FileHandler(log_file, "a")
        fh.setLevel(logging.INFO)
        return fh


class PrintHandler(object):
    """Handler for elastic prints"""
    def __init__(self, logging_level):
        self.ch = self._init_handler(logging_level)

    def _init_handler(self, logging_level):
        """Create log stream"""
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        return ch