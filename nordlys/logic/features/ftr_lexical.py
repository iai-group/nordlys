"""
FTR Lexical
===========

Implements lexical features (string similarities, IDF scores, ...).

:Authors: Dario Garigliotti, Faegheh Hasibi
"""

from __future__ import division
import argparse
from statistics import mean
from scipy import spatial
import numpy as np

from nordlys.config import MONGO_HOST, MONGO_DB, MONGO_COLLECTION_WORD2VEC
from nordlys.core.storage.mongo import Mongo
from nordlys.logic.features.word2vec import Word2Vec


class FtrLexical(object):
    __MAX = "max"
    __SUM = "sum"
    __AVG = "avg"
    __AGGREGATIONS = {__MAX, __SUM, __AVG}

    def __init__(self):
        self.__word2vec = None

    @property
    def word2vec(self):
        if self.__word2vec is None:
            w2v_mongo = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_WORD2VEC)
            self.__word2vec = Word2Vec(w2v_mongo)
        return self.__word2vec

    def jaccard_sim(self, s1, s2):
        """Computes the Jaccard similarity between two strings.

        :param s1: a sequence of terms.
        :type s1: str
        :param s2: another sequence of terms.
        :type s1: str
        :return:
        """
        set1, set2 = set(s1.split()), set(s2.split())
        num = len(set1.intersection(set2))
        denom = len(set1.union(set2))
        return num / denom if denom != 0 else 0

    def __cos_sim(self, v1, v2):
        """Wraps scikit-learn cosine similarity to deal with portability issues.

        :param v1: numpy array.
        :param v2: another numpy array.
        :return: a float value in the range [0, 1].
        """
        if np.count_nonzero(v1) == 0 or np.count_nonzero(v2) == 0:
            # whenever at least one of the vectors is all zeros, spatial.distance.cosine will fail by returning nan
            ret = 0
        else:
            ret = 1 - spatial.distance.cosine(v1, v2)
        return ret

    def w2v_sim(self, s1, s2):
        """Computes the word2vec similarity (cosine) of the two strings.
        For each string s a single (centroid) vector is created by averaging the term vectors for each term in s.

        :param s1: a sequence of terms.
        :type s1: str
        :param s2: another sequence of terms.
        :type s1: str
        :return:
        """
        v1 = self.word2vec.get_centroid_vector(s1)
        v2 = self.word2vec.get_centroid_vector(s2)
        return self.__cos_sim(v1, v2)

    def agg(self, values, agg_func):
        """Aggregates a list of values.

        :param values: a non-empty list of values.
        :type values: list
        :param agg_func: the aggregation function name, with value in {"max", "sum", "avg"}. Average by default.
        :type agg_func: str
        :return: aggregated result
        """
        assert len(values) > 0, "Empty list of values"
        f = agg_func.strip().lower()
        assert f in self.__AGGREGATIONS, "Aggregation function " + agg_func + " is not valid"

        ret = 0  # just to avoid "Local variable might be referenced before assignment" warning
        if f == self.__MAX:
            ret = max(values)
        elif f == self.__SUM:
            ret = sum(values)
        elif f == self.__AVG:
            ret = mean(values)
        return ret

    def edit_dis_agg(self, s1, s2, agg_func=__AVG):
        """Computes Jaro distance.

        :param s1: a sequence of terms.
        :type s1: str
        :param s2: another sequence of terms.
        :type s1: str
        :param agg_func: the aggregation function name, with value in {"max", "sum", "avg"}. Average by default.
        :type agg_func: str
        :return: the distance value.
        """
        res = []
        for t1 in s1.split():
            for t2 in s2.split():
                res.append(jf.jaro_distance(t1, t2))
        return self.agg(res, agg_func)

    def w2v_sim_agg(self, s1, s2, agg_func=__AVG):
        """Computes word2vec similarity for each two terms in the strings.

        :param s1: a sequence of terms.
        :type s1: str
        :param s2: another sequence of terms.
        :type s1: str
        :param agg_func: the aggregation function name, with value in {"max", "sum", "avg"}. Average by default.
        :type agg_func: str
        :return: the aggregated similarity.
        """
        res = []
        for t1 in s1.split():
            v1 = self.word2vec.get_vector(t1)
            for t2 in s2.split():
                v2 = self.word2vec.get_vector(t2)
                res.append(self.__cos_sim(v1, v2))
        return self.agg(res, agg_func)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sim", help="two words, for showing their w2v cosine similarity", type=str)
    parser.add_argument("-w", "--w2vaggrsim", help="two words, for showing their aggr. w2v cosine similarity", type=str)
    parser.add_argument("-j", "--jaccard", help="two words, for showing their Jaccard similarity", type=str)
    parser.add_argument("-e", "--edit", help="two words, for showing their edit similarity", type=str)
    args = parser.parse_args()
    return args


def main(args):
    # word2vec main __instances
    feat = FtrLexical()
    print("\t\t*** Lexical features functionalities. ***\n")

    # Testing some functionalities
    w1, w2 = "", ""
    sim = 0
    if args.sim:
        w1, w2 = args.sim.split(maxsplit=2)
        w1, w2 = w1.strip(), w2.strip()
        sim = feat.w2v_sim(w1, w2)
    elif args.w2vaggrsim:
        w1, w2 = args.w2vaggrsim.split(maxsplit=2)
        w1, w2 = w1.strip(), w2.strip()
        sim = feat.w2v_sim_agg(w1, w2)
    elif args.jaccard:
        w1, w2 = args.jaccard.split(maxsplit=2)
        w1, w2 = w1.strip(), w2.strip()
        sim = feat.jaccard_sim(w1, w2)
    elif args.edit:
        w1, w2 = args.edit.split(maxsplit=2)
        w1, w2 = w1.strip(), w2.strip()
        sim = feat.edit_dis_agg(w1, w2)
    print("words = {}, {}\n"
          "similarity = {}\n".format(w1, w2, sim))


if __name__ == "__main__":
    main(arg_parser())
