"""
Entity Retrieval
================

Abstract class for entity retrieval.

:Author: Krisztian Balog
"""

import abc


class EntityRetrieval(metaclass=abc.ABCMeta):

    def __init__(self, config):
        self.__config = config

    @abc.abstractmethod
    def retrieve(self, query, num=1000):
        """Returns a ranked list of entities with retrieval scores.

        :param query: query string
        :param num: number of hits to return (default: 1000)
        :return:
        """
        return
