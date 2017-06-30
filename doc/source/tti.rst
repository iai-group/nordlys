Target Type Identification
==========================

A characteristic property of entities is that they are typed. Naturally, entity-bearing queries may be complemented with target types (types of its relevant entities).
Given a search query, *Target Type Identification* (TTI) is the task of returning a ranked list of types from an underlying type taxonomy.
Entity retrieval performance can be significantly improved when explicit target type information is identified for a query.

The following methods for target type identification are implemented in Nordlys:

- **EC**: the Entity Centric (EC) method, as described in [:ref:`Balog and Neumayer, 2012 <ref_Balog2012>`]. Both BM25 and LM models can be used as a retrieval model. This method fits the late fusion design pattern in [:ref:`Zhang and Balog, 2017 <ref_Zhang2017>`].
- **TC**: the Type Centric (TC) method based on [:ref:`Balog and Neumayer, 2012 <ref_Balog2012>`]. Both BM25 and LM models can be used as a retrieval model. This method fits the early fusion design pattern in [:ref:`Zhang and Balog, 2017 <ref_Zhang2017>`].
- **LTR**: the Learing-To-Rank (LTR) method, as proposed in [:ref:`Garigliotti et al., 2017 <ref_Garigliotti2017>`]. This method establishes the state-of-the-art performance in TTI.



Usage
-----

- :doc:`Command line usage <api/nordlys.services.tti>`
- :ref:`API usage <api_tti>`


Benchmark results
-----------------

Below, we present retrieval results on the target type identification in [:ref:`Garigliotti et al., 2017 <ref_Garigliotti2017>`].

+---------------------+------------+-------------+
| Method              | NDCG@1     | NDCG@5      |
+=====================+============+=============+
| EC, BM25 (*K = 20*) | 0.1490     | 0.3223      |
+---------------------+------------+-------------+
| EC, LM (*K = 20*)   | 0.1417     | 0.3161      |
+---------------------+------------+-------------+
| TC, BM25            | 0.2015     | 0.3109      |
+---------------------+------------+-------------+
| TC, LM              | 0.2341     | 0.3780      |
+---------------------+------------+-------------+
| LTR                 | **0.4842** | **0.6355**  |
+---------------------+------------+-------------+



The corresponding files with rankings can be found on `Github <https://github.com/iai-group/sigir2017-query_types>`_, specifically under `output` directory.


References
----------

.. _ref_Garigliotti2017:

- Darío Garigliotti, Faegheh Hasibi, and Krisztian Balog. **Target Type Identification for Entity-Bearing Queries**. In: *40th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR ’17)*. `[BIB] <http://krisztianbalog.com/showpub.php?id=Garigliotti:2017:TTI>`_ `[PDF] <http://krisztianbalog.com/files/sigir2017-qt.pdf>`_

.. _ref_Balog2012:

- Krisztian Balog, Robert Neumayer. 2012. **Hierarchical target type identification for entity-oriented queries**. In *Proceedings of the 21st ACM International Conference on Information and Knowledge Management (CIKM '12). 2391–2394.* `[BIB] <http://krisztianbalog.com/showpub.php?id=Balog:2012:HTT>`_ `[PDF] <http://krisztianbalog.com/files/cikm2012-querytypes.pdf>`_

.. _ref_Zhang2017:

- Shuo Zhang and Krisztian Balog. **Design Patterns for Fusion-Based Object Retrieval**. In: *Jose J. et al. (eds) Advances in Information Retrieval (ECIR '17). Lecture Notes in Computer Science, vol 10193. Springer, Cham. 684-690*. `[BIB] <http://krisztianbalog.com/showpub.php?id=Zhang:2017:DPF>`_ `[PDF] <http://krisztianbalog.com/files/ecir2017-fusion.pdf>`_
