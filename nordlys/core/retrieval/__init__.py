"""
This package provides basic indexing and scoring functionality based on Elasticsearch. It can be used both for documents and for entities (as the latter are represented as fielded documents).

Indexing
--------

.. todo:: Explain indexing (representing entities as fielded documents, mongo to elasticsearch)

The :mod:`~nordlys.core.retrieval.toy_indexer` module provides a toy example.


Notes
~~~~~

* There is no need to create a separate *id* field for document IDs. Elasticsearch creates an ``_id`` field by default.
* You may ignore creating a separate *catch-all* field. Elasticsearch automatically creates a catch-all field (called ``_all``), which is not stored; see the `elasticsearch documentation <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-all-field.html>`_ for further details.
* To speed up indexing, use :meth:`~nordlys.core.retrieval.elastic.Elastic.add_docs_bulk`. The optimal number of documents to send in a single bulk depends on the size of documents; you need to figure it out experimentally.
* For indexing documents from a MongoDB collection, always use the :mod:`~nordlys.core.retrieval.indexer_mongo` module. For example usage of this class, see :mod:`~nordlys.core.data.dbpedia.indexer_fsdm`.
* We strongly recommend using the default Elasticsearch similarity (currently BM25) for indexing. (`Other similarity functions <https://www.elastic.co/guide/en/elasticsearch/reference/2.3/index-modules-similarity.html>`_ may be also used; in that case the similarity function can updated after indexing.)


Retrieval
---------

.. todo:: Explain two-stage retrieval


Basic retrieval models (LM, MLM, and PRMS) are implemented in the :mod:`~nordlys.core.retrieval.scorer` module. Check these out to get inspiration for writing a new scorer.


Command line usage
~~~~~~~~~~~~~~~~~~

::

	python -m nordlys.core.retrieval.retrieval data/config/eg_retrieval.config.json


* Config file contain settings for 2-phase retrieval:
	*  *first_pass*: elastic built-in retrieval
	*  *second_pass*: nordlys retrieval methods
* The retrieval model (with its parameters) should be set according to `elastic search <https://www.elastic.co/guide/en/elasticsearch/reference/2.3/index-modules-similarity.html>`_
* If *second_pass* settings are not set, only first pass retrieval is performed.


API usage
~~~~~~~~~



Notes
~~~~~

* Always use a :class:`~nordlys.core.retrieval.elastic_cache.ElasticCache` object (instead of :class:`~nordlys.core.retrieval.elastic.Elastic`) for getting stats from the index. This class stores index stats (except term frequencies) in the memory, which strongly benefits efficiency.
* For getting term frequencies, you can call the :meth:`~nordlys.core.retrieval.elastic.Elastic.term_freq` method, but it may negatively affect efficiency. This means that you are reading from the index for each document, field, and term.
* You can also use :meth:`~nordlys.core.retrieval.elastic.Elastic.term_freqs` to get term frequency for all terms of a document field and cache it in memory. This helps efficiency, but remember that it can fill up the memory quite fast.
     * The best strategy could be to cache term frequencies for each query (i.e., for every new query, all cache term frequencies should be deleted).
     * For you can read :meth:`~nordlys.core.retrieval.scorer.ScorerLM.get_lm_term_prob` for example usage.

"""
