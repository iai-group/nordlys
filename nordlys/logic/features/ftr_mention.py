"""
FTR Mention
===========

Implements mention feature.

:Author: Faegheh Hasibi
"""
from nordlys.logic.query.mention import Mention


class FtrMention(object):

    def __init__(self, mention, entity=None, cand_ens=None):
        self.__mention = mention.strip()
        self.__entity = entity
        self.__cand_ens = cand_ens

    def __load_cand_ens(self):
        """Gets candidate entities if they are not provided."""
        if self.__cand_ens is None:
            self.__cand_ens = Mention(self.__mention, self.__entity).get_cand_ens()

    def len_ratio(self, q):
        """Computes mention to query length."""
        return len(self.__mention.split()) / len(q.split())

    def mention_len(self):
        """Number of terms in the mention"""
        return len(self.__mention.split())

    def matches(self):
        """Number of entities whose surface form equals the mention.
        Uses both DBpedia and Freebase name variants.
        """
        self.__load_cand_ens()
        return len(self.__cand_ens)
