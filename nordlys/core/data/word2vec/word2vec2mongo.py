"""
word2vec2mongo
--------------

Loads Word2Vec to MongoDB.

@author: Faegheh Hasibi
@author: Dario Garigliotti
"""

import argparse
import os.path as op
from sys import exit

from nordlys.config import MONGO_HOST, MONGO_DB, MONGO_COLLECTION_WORD2VEC
from nordlys.core.storage.mongo import Mongo
from nordlys.core.utils.file_utils import FileUtils

KEY_COLLECTION = "collection"
KEY_MAPPING_FILE = "mapping_file"


class Word2VecToMongo(object):
    def __init__(self, config):
        self.__check_config(config)
        self.__collection = config[KEY_COLLECTION]
        self.__w2v_fname = config[KEY_MAPPING_FILE]
        self.__mongo = None

    @staticmethod
    def __check_config(config):
        """Checks params and set default values."""
        try:
            if KEY_COLLECTION not in config:
                raise Exception(KEY_COLLECTION + " is missing")
            if KEY_MAPPING_FILE not in config:
                raise Exception(KEY_MAPPING_FILE + " is missing")
            if not op.exists(config[KEY_MAPPING_FILE]):
                raise Exception("Mapping file path does not exist.")
        except Exception as e:
            print("Error in config file: ", e)
            exit(1)
        return config

    def __parse_line(self, line):
        """
        Parses a line of the plain-text GoogleNews 300-dim pre-trained corpus.

        :param line:
        :type line: string
        :return: a (word, vector) tuple.
        """
        word, vec_str = line.rstrip().split(maxsplit=1)
        vector = [float(x) for x in vec_str.split()]

        return word, vector

    def build(self):
        """Builds word2vec collection from GoogleNews 300-dim pre-trained corpus."""
        self.__mongo = Mongo(MONGO_HOST, MONGO_DB, self.__collection)
        self.__mongo.drop()

        infile = FileUtils.open_file_by_type(self.__w2v_fname)
        i = 0
        for line in infile:
            term, vector = self.__parse_line(line)
            self.__mongo.add(term, {'vector': vector})
            i += 1
            if i % 1000 == 0:
                print(str(i / 1000) + "K lines are loaded.")
                # break
                pass


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="word2vec corpus filename", type=str)
    args = parser.parse_args()
    return args


def main(args):
    config = FileUtils.load_config(args.config)
    w2v_to_mongo = Word2VecToMongo(config)
    w2v_to_mongo.build()


if __name__ == '__main__':
    main(arg_parser())
