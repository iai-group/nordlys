Installation
============

Nordlys is a general-purpose semantic search toolkit, which can be deployed on a local machine. There is built-in support for certain data collections, including DBpedia and Freebase. You may download these data sets and run a set of scripts for preprocessing and indexing them, as explained below. Alternatively, you may use the data dumps we made available; since those are huge, they are not on git but are available at a separate location (see below).

1. Obtain source code
~~~~~~~~~~~~~~~~~~~~~

You can clone the Nordlys repo using the following: ::

  $ git clone https://github.com/iai-group/nordlys.git


2. Install prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~

Before deploying Nordlys, make sure the follwoings are installed on your machine:

- `Python Anaconda distribution <https://docs.continuum.io/anaconda/install>`_
- `MongoDB <https://docs.mongodb.com/manual/installation/>`_
- `Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/2.3/_installation.html>`_

Then install Nodlys prerequisites using pip: ::

  $ pip install -r requirements.txt

If you don't have pip yet, install it using ::

  $ easy_install pip

.. note:: On Ubuntu, you might need to install lxml using a package manager ::

      $ apt-get install python-lxml


3. Load data
~~~~~~~~~~~~

Load DBpedia to MongoDB
^^^^^^^^^^^^^^^^^^^^^^^


DBpedia is distributed, among other formats, as a set of .ttl.bz2 files.
We use a selection of these .ttl files, as defined in `data/config/dbpedia2mongo.config.json`.  You can download these files from `DBpedia Website <http://downloads.dbpedia.org/2015-10/core-i18n/en/>`_. We provide a minimal sample from DBpedia under `data/dbpedia-2015-10-sample`, which can be used for testing Nordlys on a local machine.

To load these files into mongodb, run ::

    python -m nordlys.core.data.dbpedia.dbpedia2mongo data/config/dbpedia2mongo.config.json

.. note:: You may change the `path` variable in the config file; by default it is set to the sample file directory.

See the :mod:`~nordlys.core.data.dbpedia.dbpedia2mongo` module for details.

Build indices
^^^^^^^^^^^^^

Once DBpedia is loaded into MongoDB, the following indices can be built:

- **DBpedia index**
    - Used in ER, EL, and TTI services ::

        python -m nordlys.core.data.dbpedia.indexer_dbpedia data/config/index_dbpedia_2015_10.config.json

- **DBpedia URI-only index** 
   - Used in ELR method of ER service ::

        python -m nordlys.core.data.dbpedia.indexer_dbpedia_uri data/config/index_dbpedia_2015_10_uri.config.json

- **DBpedia types index** 
    - Used in TTI service ::

        python -m nordlys.core.data.dbpedia.indexer_dbpedia_types data/config/index_dbpedia_2015_10_types.config.json


Load other MongoDB collections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A set of other collections has been used for different Nordlys services. We detail the commands used for generating these collections, yet they can be all dowloaded from the provided links.

- **Surface form dictionary (DBpedia)**
    - Used in EL service
    - Surface form dictionary, extracted from DBpedia entity name variants
    - `Download link <http://iai.group/downloads/nordlys-v02/surface_forms_dbpedia.tar.bz2>`_ ::

        python -m nordlys.core.data.dbpedia.dbpedia_surfaceforms2mongo data/config/dbpedia_surfaceforms2mongo.config.json

- **Surface form dictionary (FACC)**
    - Used in EL service
    - Surface form dictionary, extracted from FACC collection
    - `Download link <http://iai.group/downloads/nordlys-v02/surface_forms_facc.tar.bz2>`_ ::

        python -m nordlys.core.data.facc.facc2mongo data/config/facc2mongo.config.json

- **Freebase to DBpedia mapping**
    - Used in EL service
    - Contains mapping of Freebase to DBpedia IDs 
    - `Download link <http://iai.group/downloads/nordlys-v02/fb2dbp-2015-10.tar.bz2>`_ ::

        python -m nordlys.core.data.dbpedia.freebase2dbpedia2mongo  data/config/freebase2dbpedia2mongo.config.json


- **Word2Vec (Google news- 300D)**
   - Used in LTR methods for EL, ES, and TTI services
   - Contains mapping of terms to their word-embedding vectors
   - `Download link <http://iai.group/downloads/nordlys-v02/word2vec-googlenews.tar.bz2>`_ ::

        python -m nordlys.core.data.word2vec.word2vec2mongo data/config/word2vec2mongo.config.json
