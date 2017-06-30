"""
Top Fields
==========

This class returns top fields based on document frequency

:Author: Faegheh Hasibi
"""
from nordlys.core.retrieval.elastic import Elastic
from nordlys.config import PLOGGER


class TopFields(object):
    DEBUG = 0

    def __init__(self, elastic):
        self.elastic = elastic
        self.__fields = None
        self.__fsdm_fields = {"names", "categories", "attributes", "similar_entity_names", "related_entity_names"}

    @property
    def fields(self):
        if self.__fields is None:
            self.__fields = set(self.elastic.get_fields())
        return self.__fields

    def get_top_term(self, en, n):
        """Returns top-n fields with highest document frequency for the given entity ID."""
        doc_freq = {}
        if self.DEBUG:
            PLOGGER.info("Entity:[" + en + "]")
        for field in self.fields:
            df = self.elastic.doc_freq(en, field)
            if df > 0:
                doc_freq[field] = df
        top_fields = self.__get_top_n(doc_freq, n)
        return top_fields

    def __get_top_n(self, fields_freq, n):
        """Sorts fields and returns top-n."""
        sorted_fields = sorted(fields_freq.items(), key=lambda item: (item[1], item[0]), reverse=True)
        top_fields = dict()
        i = 0
        for field, freq in sorted_fields:
            if i >= n:
                break
            if field in self.__fsdm_fields:
                continue
            i += 1
            top_fields[field] = freq
            if self.DEBUG:
                print("(" + field + ", " + str(freq) + ")")
        if self.DEBUG:
            PLOGGER.debug("\nNumber of fields:", len(top_fields), "\n")
        return top_fields
