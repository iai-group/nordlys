"""
Commonness Entity Linking Approach
==================================

Class for commonness entity linking approach

:Author: Faegheh Hasibi
"""
from collections import defaultdict

import sys

from nordlys.logic.entity.entity import Entity
from nordlys.logic.query.mention import Mention
from nordlys.logic.query.query import Query


class Cmns(object):
    def __init__(self, query, entity, cmns_th=0.1):
        self.__query = query
        self.__entity = entity
        self.__cmns_th = cmns_th
        self.__ngrams = None
        self.__ranked_ens = {}
        self.__mentions = set()

    def link(self):
        """Links the query to the entity.

        dictionary {mention: (en_id, score), ..}
        """
        self.rank_ens()
        linked_ens = self.disambiguate()
        return linked_ens

    def rank_ens(self):
        """Detects mention and rank entities for each mention"""
        self.__get_ngrams()
        self.__recursive_rank_ens(len(self.__query.query.split()))

    def __get_ngrams(self):
        """Returns n-grams grouped by length.

        :return: dictionary {1:["xx", ...], 2: ["xx yy", ...], ...}
        """
        if self.__ngrams is None:
            self.__ngrams = defaultdict(list)
            for ngram in self.__query.get_ngrams():
                self.__ngrams[len(ngram.split())].append(ngram)

    def __recursive_rank_ens(self, n):
        """Generates list of entities for each mention in the query.

        The algorithm starts from the longest possible n-gram and gets all matched entities.
        If no entities found, the algorithm recurse and tries to find entities with (n-1)-gram.

        :param n: length of n-gram
        :return: dictionary {(dbp_uri, fb_id):commonness, ..}
        """
        if n == 0:
            return

        for ngram in self.__ngrams[n]:
            if not self.__is_overlapping(ngram):
                cand_ens = Mention(ngram, self.__entity, self.__cmns_th).get_cand_ens()
                if len(cand_ens) > 0:
                    self.__ranked_ens[ngram] = cand_ens
                    self.__mentions.add(ngram)
        self.__recursive_rank_ens(n - 1)

    def disambiguate(self):
        """Selects only one entity per mention.

        :return [{"mention": xx, "entity": yy, "score": zz}, ...] #dictionary {mention: (en_id, score), ..}
        """
        linked_ens = []  # {}
        for men, ens in self.__ranked_ens.items():
            sorted_ens = sorted(ens.items(), key=lambda x: x[1], reverse=True)
            linked_ens.append({"mention": men, "entity": sorted_ens[0][0], "score": sorted_ens[0][1]})
            # linked_ens[men] = sorted_ens[0]
        return linked_ens

    def __is_overlapping(self, ngram):
        """Checks whether the ngram is contained in one of the currently identified mentions."""
        for mention in self.__mentions:
            if ngram in mention:
                return True
        return False

def main(args):
    entity = Entity()
    query = Query(args[0])
    cmns = Cmns(query, entity, cmns_th=0.1)
    print(cmns.link())

if __name__ == "__main__":
    main(sys.argv[1:])
