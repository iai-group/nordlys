"""
elastic_cache
-------------

This is a cache for elastic index stats; a layer between an index and scorer.

@author: Faegheh Hasibi
"""
from collections import defaultdict
from nordlys.core.retrieval.elastic import Elastic


class ElasticCache(Elastic):
    def __init__(self, index_name):
        super(ElasticCache, self).__init__(index_name)

        # Cached variables
        self.__num_docs = None
        self.__num_fields = None
        self.__doc_count = {}
        self.__coll_length = {}
        self.__avg_len = {}
        self.__doc_length = defaultdict(dict)
        self.__tv = defaultdict(dict)
        self.__coll_tv = defaultdict(dict)

    def __get_termvector(self, doc_id, field):
        """Returns a term vector for a given document and field."""
        if self.__tv.get(doc_id, {}).get(field, None) is None:
            self.__tv[doc_id][field] = self._get_termvector(doc_id, field)
        return self.__tv[doc_id][field]

    def __get_coll_termvector(self, term, field):
        """Returns a term vector containing collection stats of a term."""
        if self.__coll_tv.get(term, {}).get(field, None) is None:
            self.__coll_tv[term][field] = self._get_coll_termvector(term, field)
        return self.__coll_tv[term][field]

    def num_docs(self):
        """Returns the number of documents in the index."""
        if self.__num_docs is None:
            self.__num_docs = super(ElasticCache, self).num_docs()
        return self.__num_docs

    def num_fields(self):
        """Returns number of fields in the index."""
        if self.__num_fields is None:
            self.__num_fields = super(ElasticCache, self).num_fields()
        return self.__num_fields

    def doc_count(self, field):
        """Returns number of documents with at least one term for the given field."""
        if field not in self.__doc_count:
            self.__doc_count[field] = super(ElasticCache, self).doc_count(field)
        return self.__doc_count[field]

    def coll_length(self, field):
        """Returns length of field in the collection."""
        if field not in self.__coll_length:
            self.__coll_length[field] = super(ElasticCache, self).coll_length(field)
        return self.__coll_length[field]

    def avg_len(self, field):
        """Returns average length of a field in the collection."""
        if field not in self.__avg_len:
            self.__avg_len[field] = super(ElasticCache, self).avg_len(field)
        return self.__avg_len[field]

    def doc_length(self, doc_id, field):
        """Returns length of a field in a document."""
        if self.__doc_length.get(doc_id, {}).get(field, None) is None:
            self.__doc_length[doc_id][field] = sum(self.term_freqs(doc_id, field).values())
        return self.__doc_length[doc_id][field]

    def doc_freq(self, term, field, tv=None):
        """Returns document frequency for the given term and field."""
        tv = self.__get_coll_termvector(term, field)
        return super(ElasticCache, self).doc_freq(term, field, tv=tv)

    def coll_term_freq(self, term, field, tv=None):
        """ Returns collection term frequency for the given field."""
        tv = self.__get_coll_termvector(term, field)
        return super(ElasticCache, self).coll_term_freq(term, field, tv=tv)

    def term_freqs(self, doc_id, field, tv=None):
        """Returns term frequencies for a given document and field."""
        tv = self.__get_termvector(doc_id, field)
        return super(ElasticCache, self).term_freqs(doc_id, field, tv)

    def term_freq(self, doc_id, field, term):
        """Returns frequency of a term in a given document and field."""
        return self.term_freqs(doc_id, field).get(term, 0)
