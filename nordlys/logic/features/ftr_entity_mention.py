"""
FTR Entity Mention
==================

Implements features related to an entity-mention pair.

:Author: Faegheh Hasibi
"""

from nordlys.logic.query.query import Query


TITLE = "<rdfs:label>"
SHORT_ABS = "<rdfs:comment>"


class FtrEntityMention(object):

    def __init__(self, en_id, mention, entity):
        self.__en_id = en_id
        self.__mention = mention
        self.__entity = entity
        self.__en_doc = None

    def __load_en(self):
        if self.__en_doc is None:
            en_doc = self.__entity.lookup_en(self.__en_id)
            self.__en_doc = en_doc if en_doc is not None else {}

    def commonness(self):
        """Computes probability of entity e being linked by mention: link (e,m)/link(m)
        Returns zero if link(m) = 0
        """
        fb_ids = self.__entity.dbp_to_fb(self.__en_id)
        if fb_ids is None:
            return 0
        matches = self.__entity.lookup_name_facc(self.__mention).get("facc12", {})
        total_occurrences = sum(list(matches.values()))
        commonness = matches.get(fb_ids[0], 0) / total_occurrences if total_occurrences != 0 else 0
        return commonness

    def mct(self):
        """Returns True if mention contains the title of entity """
        self.__load_en()
        mct = 0
        en_title = Query(self.__en_doc.get(TITLE, [""])[0]).query
        if en_title in self.__mention:
            mct = 1
        return mct

    def tcm(self):
        """Returns True if title of entity contains mention """
        self.__load_en()
        tcm = 0
        en_title = Query(self.__en_doc.get(TITLE, [""])[0]).query
        if self.__mention in en_title:
            tcm = 1
        return tcm

    def tem(self):
        """Returns True if title of entity equals mention."""
        self.__load_en()
        tem = 0
        en_title = Query(self.__en_doc.get(TITLE, [""])[0]).query
        if self.__mention == en_title:
            tem = 1
        return tem

    def pos1(self):
        """Returns position of the occurrence of mention in the short abstract."""
        self.__load_en()
        pos1 = 1000
        s_abs = self.__en_doc.get(SHORT_ABS, [""])[0].lower()
        if self.__mention in s_abs:
            pos1 = s_abs.find(self.__mention)
        return pos1
