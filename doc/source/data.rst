Data components
===============

MongoDB collections
-------------------

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


Raw data sources
----------------

DBpedia
~~~~~~~

.. todo::

  COMPLETE

DBpedia is distributed, among other formats, as a set of .ttl.bz2 files.
We use a selection of these .ttl files, as defined in `data/config/dbpedia2mongo.config.json`.  You can download these files from `DBpedia Website <http://downloads.dbpedia.org/2015-10/core-i18n/en/>`_. We provide a minimal sample from DBpedia under `data/dbpedia-2015-10-sample`, which can be used for testing Nordlys on a local machine.


FACC
~~~~


Word2Vec
~~~~~~~~

.. todo::

  Google news- 300D
