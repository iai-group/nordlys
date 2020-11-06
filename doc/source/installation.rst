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
- `Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/5.5/_installation.html>`_

Then install Nordlys prerequisites using pip: ::

  $ pip install -r requirements.txt

If you don't have pip yet, install it using ::

  $ easy_install pip

.. note:: On Ubuntu, you might need to install lxml using a package manager ::

      $ apt-get install python-lxml


2.1 Configure MongoDB
~~~~~~~~~~~~~~~~~~~~~

Adjust the settings in `config/mongo.json`, if needed.

If you're using macOS, you'll likely need to change the soft limit of maxfiles to at least 64000, for mongoDB to work properly. Check the maxfiles limit of your system using: ::

    $ launchctl limit



2.2 Configure Elasticsearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adjust the settings in `config/elastic.json`, if needed.

Note that Elasticsearch requires Java version 8.


3. Load data
------------

Data are a crucial component of Nordlys.  Note that you may need only a certain subset of the data, depending on the required functionality.  See :doc:`this page <data>` for a detailed description.

We use MongoDB and Elasticsearch for storing and indexing data. The figure below shows an overview of data sources and their dependencies.

.. figure::  figures/nordlys_load_data.png
   :align:   center
   :scale: 75%
   :alt: Nordlys data components

.. note::

  All scripts below are to be run from the nordlys main directory. ::

    nordlys-v02$ ./scripts/scriptname.sh


3.1 Load data to MongoDB
~~~~~~~~~~~~~~~~~~~~~~~~

To load the data to MongoDB, you need to run the following commands. Note that the first command is required for all Nordlys functionalities. Other commands are optional and you may run them if the mentioned functionality is needed.

+-----------------------------------------------------------------------+------------------+
| Command                                                               | Required for     |
+=======================================================================+==================+
| ``./scripts/load_mongo_dumps.sh mongo_dbpedia-2015-10.tar.bz2``       | All              |
+-----------------------------------------------------------------------+------------------+
| ``./scripts/load_mongo_dumps.sh mongo_surface_forms_dbpedia.tar.bz2`` | EL and EC        |
|                                                                       |                  |
| ``./scripts/load_mongo_dumps.sh mongo_surface_forms_facc.tar.bz2``    |                  |
|                                                                       |                  |
| ``./scripts/load_mongo_dumps.sh mongo_fb2dbp-2015-10.tar.bz2``        |                  |
+-----------------------------------------------------------------------+------------------+
| ``./scripts/load_mongo_dumps.sh mongo_word2vec-googlenews.tar.bz2``   | TTI              |
+-----------------------------------------------------------------------+------------------+


3.2 Build Elastic indices
~~~~~~~~~~~~~~~~~~~~~~~~~
The Nordlys directory by default contains a minimal sample files folder from *DBpedia 2015-10*, which can be used for testing Nordlys on a local machine.

Hence, before creating the indices, some files have to be downloaded by running the *Type-to-entity mapping sample* and *Freebase to DBpedia sample* blocks of `scripts/download_all.sh` script from the `nordlys` directory.

Alternatively, you can run: ::

./scripts/download_all.sh

This will download all data raw files of original DBpedia collection required for Nordlys.


Run the following commands to build the indices for the mentioned functionalities.

+--------------------------------------------+--------------------------+
| Command                                    | Required for             |
+============================================+==========================+
| ``./scripts/build_indices.sh dbpedia``     | ER, EL, TTI              |
+--------------------------------------------+--------------------------+
| ``./scripts/build_indices.sh types``       | TTI                      |
+--------------------------------------------+--------------------------+
| ``./scripts/build_indices.sh dbpedia_uri`` | ER (only for ELR model)  |
+--------------------------------------------+--------------------------+


3.3 Download the remaining data files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following commands to download the data file needed for running entity linking service

+------------------------------------------------------------------------------------------+--------------+
| Command                                                                                  | Required for |
+==========================================================================================+==============+
| ``wget https://gustav1.ux.uis.no/downloads/nordlys-v02/snapshot_2015_10.txt -P data/el`` | EL           |
+------------------------------------------------------------------------------------------+--------------+


3.4 Create folders for logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a folder named ``logs`` and a sub-folder named ``api`` in Nordlys main directory, for the log files that'll be generated by the API.
