"""
Retrieval
=========

The retrieval package provides basic indexing and scoring functionality based on Elasticsearch (v2.3).
It can be used both for documents and for entities (as the latter are represented as fielded documents).


Indexing
--------

Indexing can be done be done by directly reading the content of documents.
The :mod:`~nordlys.core.retrieval.toy_indexer` module provides a toy example.

When the content of documents is stored in MongoDB (e.g., for DBpedia entities), use the :mod:`~nordlys.core.retrieval.indexer_mongo` module for indexing.
For further details on how this module can be used, see :mod:`~nordlys.core.data.dbpedia.indexer_dbpedia`.

For indexing Dbpedia entities, we read the content of entiteis form MongoDB aFor DBpedia entities, we store them on MongoDB and
.. todo:: Explain indexing (representing entities as fielded documents, mongo to elasticsearch)

Notes
~~~~~

- To speed up indexing, use :meth:`~nordlys.core.retrieval.elastic.Elastic.add_docs_bulk`. The optimal number of documents to send in a single bulk depends on the size of documents; you need to figure it out experimentally.
- We strongly recommend using the default Elasticsearch similarity (currently BM25) for indexing. (`Other similarity functions <https://www.elastic.co/guide/en/elasticsearch/reference/2.3/index-modules-similarity.html>`_ may be also used; in that case the similarity function can updated after indexing.)
- Our default setting is *not* to store term positions in the index (for efficiency considerations).


Retrieval
---------

Retrieval is done in two stages:

- *First pass*: The top ``N`` documents are retrieved using Elastic's default search method
- *Second pass*: The (expensive) scoring of the top ``N`` documents is performed (implemented in the Nordlys)


Nordlys currently supports the following models for second pass retrieval:

- Language modelling (LM) [1]
- Mixture of Language Modesl (MLM) [2]
- Probabilistic Model for Semistructured Data (PRMS) [3]

Check out :mod:`~nordlys.core.retrieval.scorer` module to get inspiration for implementing a new retrieval model.


Command line usage
~~~~~~~~~~~~~~~~~~

See :py:mod:`nordlys.core.retrieval.retrieval`


Notes
~~~~~

- Always use a :class:`~nordlys.core.retrieval.elastic_cache.ElasticCache` object (instead of :class:`~nordlys.core.retrieval.elastic.Elastic`) for getting stats from the index. This class stores index stats in the memory, which highly benefits efficiency.
- We recommend to create a new :class:`~nordlys.core.retrieval.elastic_cache.ElasticCache` object for each query. This way, you will make effiecnt of your machine's memory.

-------------------

[1] Jay M Ponte and W Bruce Croft. 1998. *A Language modeling approach to information retrieval*. In Proc. of SIGIR '98.

[2] Paul Ogilvie and Jamie Callan. 2003. *Combining document representations for known-item search*. Proc. of SIGIR '03.

[3] Jinyoung Kim, Xiaobing Xue, and W Bruce Croft. 2009. *A probabilistic retrieval model for semistructured data*. In Proc. of ECIR '09.

"""
