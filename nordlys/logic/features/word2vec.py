"""
word2vec
---------

Implements functionalities over the 300-dim GoogleNews word2vec semantic representations of words.

@author: Dario Garigliotti
"""

import argparse
import numpy as np

from nordlys.config import MONGO_HOST, MONGO_DB, MONGO_COLLECTION_WORD2VEC
from nordlys.core.storage.mongo import Mongo


class Word2Vec(object):
    __DIMENSION = 300  # Dimension of GoogleNews pre-trained corpus vectors

    def __init__(self, mongo):
        self.__mongo_collection = mongo

    def get_vector(self, word):
        """Gets the w2v vector corresponding to the word, or a zero-valued vector if not present.

        :param word: a word.
        :type word: str
        :return:
        """
        doc = self.__mongo_collection.find_by_id(word)
        return np.array(doc["vector"]) if doc is not None else np.zeros((self.__DIMENSION,))

    def get_centroid_vector(self, s):
        """
        Returns the normalized sum of the word2vec vectors corresponding to the terms in s.

        :param s: a phrase.
        :type s: str
        :return: Centroid vector of the terms in s.

        """
        words = s.split()
        return (sum([self.get_vector(word) for word in words]) / len(words) if len(words) > 0
                else np.zeros((self.__DIMENSION,)))


def main(args):
    # word2vec main __instances
    w2v_mongo = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_WORD2VEC)
    w2v = Word2Vec(w2v_mongo)
    print("\t\t*** word2vec functionalities, with word vectors from GoogleNews 300-dim pre-trained corpus. ***\n")

    # Testing some functionalities
    if args.word:
        word = args.word.strip()
        vector = w2v.get_vector(word)

        print("word = {}\nvector = {}\nvector dimension = {}\n".format(word, vector, vector.shape[0]))

    if args.centroid:
        str = args.centroid.strip()
        centroid_v = w2v.get_centroid_vector(str)
        print("expression = {}\ncentroid vector = {}\n".format(str, centroid_v))


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--word", help="a word, for showing its w2v vector", type=str)
    parser.add_argument("-c", "--centroid", help="a string, for showing its centroid vector", type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main(arg_parser())
