"""
FTR Mention Entity
==================

Implements mention-entity features.

:Authors: Faegheh Hasibi, Krisztian Balog
"""
from nordlys.logic.entity.entity import Entity
from nordlys.config import MONGO_COLLECTION_SF_FACC
from nordlys.config import PLOGGER


class FtrMentionEntity(object):

    def __init__(self, sf, sources):
        self.__sf = sf
        self.__sources = sources

    def commonness(self, e, m):
        """Computes probability of entity e being linked by mention: link (e,m)/link(m)
            Returns zero if link(m)

        :param e: entity id
        :type e: str
        :param m: mention
        :type m: str
        :return: commonness
        """
        # todo: caching for link_m
        sf_lookup = self.__sf.lookup(m)
        if sf_lookup is None:
            return 0

        link_e_m = sum([sf_lookup.get(s, {}).get(e, 0) for s in self.__sources])
        link_m = sum([sum(sf_lookup.get(s, {}).values()) for s in self.__sources])
        PLOGGER.info(link_e_m, link_m)
        return link_e_m / link_m


def main():
    sf = Entity(MONGO_COLLECTION_SF_FACC)
    men_en = FtrMentionEntity(sf, sources=['facc12'])
    print(men_en.commonness("/m/0ngyw16", "009 re:cyborg"))


if __name__ == "__main__":
    main()
