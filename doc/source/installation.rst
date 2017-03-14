Installation
============

Prerequisites
-------------

  * Python Anaconda distribution
  * MongoDB
  * Elasticsearch


Installation
------------

1. Obtain source code
~~~~~~~~~~~~~~~~~~~~~

You can clone the Nordlys repo using the following: ::

  $ git clone git@bitbucket.org:kbalog/nordlys.git


2. Install prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way of installing the python prerequisites is using pip: ::

  $ pip install -r requirements.txt

If you don't have pip yet, install it using ::

  $ easy_install pip

Notes:

  - On Ubuntu, you might need to install lxml using a package manager ::

      $ apt-get install python-lxml


3. Install the package locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(You only need to do it if you want to use it from Python code) ::

  $ python setup.py install


General usage
-------------

From the command line
~~~~~~~~~~~~~~~~~~~~~

From the command line, under the nordlys main directory, use the `-m` option to run the modules as scripts. E.g., ::

  $ python -m nordlys.parse.nt_parser

.. todo:: add reference to detailed documentation

From web API
~~~~~~~~~~~~

.. todo:: add example plus reference to detailed documentation


From Python code
~~~~~~~~~~~~~~~~

Just import the modules you need, e.g., ::


  from nordlys.entity.entity import Entity
  from nordlys.entity.freebase.utils import FreebaseUtils


Load data
---------

.. todo:: Explain that you can 1) download the original data files (DBpedia, FACC, etc.) and load them or 2) download the complete data dump from XXX.

Load DBpedia into MongoDB
~~~~~~~~~~~~~~~~~~~~~~~~~

A small sample of DBpedia-2015-10 is shipped with Nordlys, to get you going. Loading the full DBpedia takes several hours. ::


  python -m nordlys.core.data.dbpedia.dbpedia2mongo data/config/dbpedia2mongo.config.json


.. todo:: create config file for full DBpedia.
