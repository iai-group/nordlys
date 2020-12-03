Data components
===============

Data sources
------------

DBpedia
~~~~~~~

We use DBpedia as the main underlying knowledge base.  In particular, we prepared dumps for DBpedia version 2015-10.

DBpedia is distributed, among other formats, as a set of .ttl.bz2 files.  We use a selection of these files, as defined in ``data/config/dbpedia2mongo.config.json``.  You can download these files from `DBpedia Website <http://downloads.dbpedia.org/2015-10/core-i18n/en/>`_ directly or running ``./scripts/download_dbpedia.sh`` from the main Nordlys folder.  Running the script will place the downloaded files under ``data/raw-data/dbpedia-2015-10/``.

We also provide a minimal sample from DBpedia under ``data/dbpedia-2015-10-sample``, which can be used for testing/development in a local environment.


FACC
~~~~
The Freebase Annotations of the ClueWeb Corpora (FACC) is used for building entity surface form dictionary. You can download the collection from its `main Website <http://lemurproject.org/clueweb12/FACC1/>`_. and further process it using our scripts. Alternatively, you can download the preprocessed data from our server.  Check the README file under `data/raw-data/facc` for detailed information.

Word2Vec
~~~~~~~~
Word2Vec vectors (300D) trained on Google News corpus, which canbe dowloaded from the its `Website <https://github.com/mmihaltz/word2vec-GoogleNews-vectors>`_. Check the README file under `data/raw-data/word2vec` for detailed information.


MongoDB collections
-------------------

The table below provides an overview of the MongoDB collections that are used by the different services.

+---------------------------+--------------------------------------+---------------+---------------+---------------+---------------+
| Name                      | Description                          | EC            | ER            | EL            | TTI           |
+===========================+======================================+===============+===============+===============+===============+
| ``dbpedia-2015-10``       | DBpedia                              | **+**:sup:`1` | **+**:sup:`2` |               | **+**:sup:`3` |
+---------------------------+--------------------------------------+---------------+---------------+---------------+---------------+
| ``fb2dbp-2015-10``        | Mapping from Freebase to DBpedia IDs | **+**:sup:`4` |               | **+**         |               |
+---------------------------+--------------------------------------+---------------+---------------+---------------+---------------+
| ``surface_forms_dbpedia`` | Entity surface forms from DBpedia    | **+**:sup:`5` |               | **+**:sup:`6` |               |
+---------------------------+--------------------------------------+---------------+---------------+---------------+---------------+
| ``surface_forms_facc``    | Entity surface forms from FACC       | **+**:sup:`7` |               | **+**         |               |
+---------------------------+--------------------------------------+---------------+---------------+---------------+---------------+
| ``word2vec-googlenews``   | Word2vec trained on Google News      |               |               |               | **+**:sup:`8` |
+---------------------------+--------------------------------------+---------------+---------------+---------------+---------------+

- :sup:`1` for entity ID-based lookup and DBpedia2Freebase mapping functionalities
- :sup:`2` only for building the Elastic entity index; not used later in the retrieval process
- :sup:`3` for entity-centric TTI method
- :sup:`4` for Freebase2DBpedia mapping functionality
- :sup:`5` for entity surface form lookup from DBpedia
- :sup:`6` for all EL methods other than "commonness"
- :sup:`7` for entity surface form lookup from FACC
- :sup:`8` for LTR TTI method


.. _data_to_mongo:
Building MongoDB sources from raw data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build the above tables from raw data (as opposed to the provided dumps), first make sure that you have the raw data files.

- For DBpedia, these may be downloaded using ``./scripts/download_dbpedia.sh``
- For the FACC and Word2vec data files, execute ``./scripts/download_raw.sh``

To load DBpedia to MongoDB, run ::

    python -m nordlys.core.data.dbpedia.dbpedia2mongo data/config/dbpedia-2015-10/dbpedia2mongo.config.json

.. note:: To use the DBpedia 2015-10 sample shipped with Nordlys, as opposed to the full collection, change the value ``path`` to ``data/raw-data/dbpedia-2015-10_sample/`` in ``dbpedia2mongo.config.json``.



.. _elastic_indices:
Elastic indices
---------------

+---------------------------+-------------------------+---------------+---------------+---------------+
| Name                      | Description             | ER            | EL            | TTI           |
+===========================+=========================+===============+===============+===============+
| ``dbpedia_2015_10``       | DBpedia index           | **+**         | **+**:sup:`1` | **+**:sup:`2` |
+---------------------------+-------------------------+---------------+---------------+---------------+
| ``dbpedia_2015_10_uri``   | DBpedia URI-only index  | **+**:sup:`3` |               |               |
+---------------------------+-------------------------+---------------+---------------+---------------+
| ``dbpedia_2015_10_types`` | DBpedia types index     |               |               | **+**:sup:`4` |
+---------------------------+-------------------------+---------------+---------------+---------------+

- :sup:`1` for all EL methods other than "commonness"
- :sup:`2` only for entity-centric TTI method
- :sup:`3` only for ELR entity ranking method
- :sup:`4` only for type-centric TTI method


