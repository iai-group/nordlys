Installation
============

Nordlys is a general-purpose semantic search toolkit, which can be deployed on a local machine. There is built-in support for certain data collections, including DBpedia and Freebase. You may download these data sets and run a set of scripts for preprocessing and indexing them, as explained below. Alternatively, you may use the data dumps we made available; since those are huge, they are not on git but are available at a separate location (see below).

1. Obtain source code
---------------------

You can clone the Nordlys repo using the following: ::

  $ git clone https://github.com/iai-group/nordlys.git


2. Install prerequisites
------------------------

Before deploying Nordlys, make sure the following ones are installed on your machine:

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
------------

Data are a crucial component of Nordlys.  Note that you may need only a certain subset of the data, depending on the required functionality.  See :doc:`this page <data>` for a detailed description.

We use MongoDB and Elasticsearch for storing and indexing data.
To load the data, you might download the raw collections from their originating sources. Alternatively, for some, we provide preprocessed versions for download.  The figure below shows an overview of data sources and their dependencies.  The raw data files may be deleted after they have been loaded into MongoDB and Elasticsearch.

.. figure::  figures/nordlys_load_data.png
   :align:   center
   :scale: 75%
   :alt: Nordlys data components

.. note::

  All scripts below are to be run from the nordlys main directory. ::

    nordlys-v02$ ./scripts/scriptname.sh


3.1 Load data to MongoDB
~~~~~~~~~~~~~~~~~~~~~~~~

To load the data to MongoDB, you may choose to to load the raw/preprocessed data using Nordlys (3.1A) or load the provided MongoDB dumps directly (3.1B).

All scripts and config files use ``nordlys-v02`` as the name of the database.

3.1A Load preprocessed data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Run ``./scripts/download_all.sh`` to download all data files.
- Run ``./scripts/load_to_mongo.sh`` to load data into MongoDB.

*If you already have a local copy of these collections, then comment out the unnecessary parts in `scripts/download_all.sh` and adjust the paths in `scripts/load_to_mongo.sh`.*

3.1B Load MongoDB dumps
^^^^^^^^^^^^^^^^^^^^^^^

- Run ``./scripts/load_mongo_dumps.sh`` to load the dumps into MongoDB.


3.2 Build Elastic indices
~~~~~~~~~~~~~~~~~~~~~~~~~

- Run ``./scripts/build_dbpedia_index.sh`` to build the ``dbpedia_2015_10`` index (required for entity ranking).
- Run ``./scripts/build_elastic_indices.sh`` to build additional Elastic indices (optional, used for certain entity and type ranking methods).
  - For this, the type-entity mapping file is needed (it is downloaded by ``./scripts/download_all.sh``; you may comment out the rest of the script just to get this file).
