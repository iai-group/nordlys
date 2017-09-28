Entity Retrieval
================

Entity retrieval is a core building block of semantic search.  Given a search query, entity retrieval is the task of returning a ranked list of entities from an underlying knowledge base.

The following entity retrieval methods are implemented in Nordlys:

- **BM25**: the default retrieval model in Elasticsearch, which uses an unstructured (single-field) entity representation. It is the most efficient retrieval model. Mind that using the default BM25 parameter settings will yield suboptimal results for entity retrieval.
- **LM**: the standard Language Modeling approach (with Dirichlet prior and Jelinek-Mercer smoothing), which employs an unstructured (single-field) entity representation.
- **MLM**: the Mixture of Language Models approach [:ref:`Ogilvie and Callan, 2003 <ref_Ogilvie2003>`], which represents entities as structured (fielded) documents, using a linear combination of language models built for each field.  Our default index configuration comprises of five fields (names, categories, similar entity names, attributes, and related entity names), plus an additional "cathall" field.
- **PRMS**: the Probabilistic Model for Semistructured Data [:ref:`Kim et al., 2009 <ref_Kim2009>`], which uses collection statistics to compute field weights for the MLM model (thereby making in parameter-free).

Nordlys provides out-of-the-box support for the DBpedia knowledge base.  It is straightforward to use it with any other knowledge base, by simply building an entity index (i.e., an Elastic index where each document corresponds to an entity).


Usage
-----

- :doc:`Command line usage <api/nordlys.services.er>`
- :ref:`API usage <api_er>`


Benchmark results
-----------------

Below, we present retrieval results on the `DBpedia-Entity v2 collection <https://github.com/iai-group/DBpedia-Entity>`_ [:ref:`Hasibi et al., 2017 <ref_Hasibi2017>`], which uses DBpedia version 2015-10.


+--------+---------+----------+
| Method | NDCG@10 | NDCG@100 |
+========+=========+==========+
| BM25   | 0.3193  | 0.3748   |
+--------+---------+----------+
| LM     | 0.4144  | 0.4880   |
+--------+---------+----------+
| MLM    | 0.3879  | 0.4661   |
+--------+---------+----------+
| MLM-TC | 0.4163  | 0.4916   |
+--------+---------+----------+
| PRMS   | 0.3717  | 0.4448   |
+--------+---------+----------+



The corresponding files may be found under `data/dbpedia-entity-v2`. Specifically:

  - ``queries_stopped.json`` contains the search queries (using stopped versions from [:ref:`Hasibi et al., 2017 <ref_Hasibi2017>`])
  - ``config`` holds the config files for the above retrieval methods
  - ``runs`` contains the corresponding output files (i.e., "run files"). These files were produced by running ``python -m nordlys.core.retrieval.retrieval data/dbpedia-entity-v2/configs/retrieval_XXX.config.json``, where ``XXX`` stands for the retrieval method (bm25, lm, mlm or prms)
  - ``qrels-v2.txt`` is the file with the relevance judgments (i.e., "v2 qrels" in [:ref:`Hasibi et al., 2017 <ref_Hasibi2017>`])
  - ``folds`` contains the folds to be used for supervised learning with cross-validation (note that the above methods do not use them).


References
----------

.. _ref_Hasibi2017:

- Faegheh Hasibi, Fedor Nikolaev, Chenyan Xiong, Krisztian Balog, Svein Erik Bratsberg, Alexander Kotov, and Jamie Callan. 2017. **DBpedia-Entity v2: A Test Collection for Entity Search**. In: *40th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR ’17)*. [`PDF <http://krisztianbalog.com/files/sigir2017-dbpedia.pdf>`_]

.. _ref_Kim2009:

- Jinyoung Kim, Xiaobing Xue, and W Bruce Croft. 2009. **A Probabilistic Retrieval Model for Semistructured Data**. In *31th European Conference on IR Research on Advances in Information Retrieval (ECIR '09)*.

.. _ref_Ogilvie2003:

- Paul Ogilvie and Jamie Callan. 2003. **Combining Document Representations for Known-Item Search**. In: *26th annual international ACM SIGIR conference on Research and development in information retrieval (SIGIR '03)*.
