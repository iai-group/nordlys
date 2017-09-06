"""
Elastic Cache
=============

This is a cache for elastic index stats; a layer between an index and retrieval.
The statistics (such as document and term frequencies) are first read from the index and stay in the memory for further
usages.



Usage hints
-----------

  - Only one instance of Elastic cache needs to be created.
  - If running out of memory, you need to create a new object of ElasticCache.
  - The class also caches termvectors. To further boost efficiency, you can load term vectors for multiple documents using :func:`ElasticCache.multi_termvector`.


:Author: Faegheh Hasibi
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
        self.__doc_freq = defaultdict(dict)
        self.__coll_term_freq = defaultdict(dict)
        self.__tv = defaultdict(dict)
        self.__coll_tv = defaultdict(dict)

    def __get_termvector(self, doc_id, field):
        """Returns a term vector for a given document and field."""
        if self.__coll_tv.get(doc_id, {}).get(field, None):
            return self.__coll_tv[doc_id][field]
        if self.__tv.get(doc_id, {}).get(field, None) is None:
            self.__tv[doc_id][field] = self._get_termvector(doc_id, field)
        return self.__tv[doc_id][field]

    def __get_coll_termvector(self, term, field):
        """Returns a term vector containing collection stats of a term."""
        body = {"query": {"bool": {"must": {"term": {field: term}}}}}
        hits = self.search_complex(body, num=1)
        doc_id = next(iter(hits.keys())) if len(hits) > 0 else None
        if self.__coll_tv.get(doc_id, {}).get(field, None) is None:
            self.__coll_tv[doc_id][field] = self._get_termvector(doc_id, field, term_stats=True) if doc_id else {}
        return self.__coll_tv[doc_id][field]

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
        if self.__doc_freq.get(field, {}).get(term, None) is None:
            tv = self.__get_coll_termvector(term, field)
            self.__doc_freq[field][term] = super(ElasticCache, self).doc_freq(term, field, tv=tv)
        return self.__doc_freq[field][term]

    def coll_term_freq(self, term, field, tv=None):
        """ Returns collection term frequency for the given field."""
        if self.__coll_term_freq.get(field, {}).get(term, None) is None:
            tv = self.__get_coll_termvector(term, field)
            self.__coll_term_freq[field][term] = super(ElasticCache, self).coll_term_freq(term, field, tv=tv)
        return self.__coll_term_freq[field][term]

    def term_freqs(self, doc_id, field, tv=None):
        """Returns term frequencies for a given document and field."""
        tv = self.__get_termvector(doc_id, field)
        return super(ElasticCache, self).term_freqs(doc_id, field, tv)

    def term_freq(self, doc_id, field, term):
        """Returns frequency of a term in a given document and field."""
        return self.term_freqs(doc_id, field).get(term, 0)

    def multi_termvector(self, doc_ids, field, batch=50):
        """Returns term vectors for a given document and field."""
        i = 0
        while i < len(doc_ids):
            j = i + batch if i + batch <= len(doc_ids) else len(doc_ids)
            tvs = self._get_multi_termvectors(doc_ids[i:j], field)
            for doc_id, tv in tvs.items():
                if tv != {}:
                    self.__tv[doc_id][field] = tv
            i += batch

