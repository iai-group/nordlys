Nordlys architecture
====================

Nordlys is based on a `multitier architecture <https://en.wikipedia.org/wiki/Multitier_architecture>`_ with three layers:

  - **core** (*data* tier)
  - **logic**
  - **services** (*presentation* tier)

.. figure::  figures/nordlys_architecture-basic.png
   :align:   center

   Nordlys architecture.


Core tier
~~~~~~~~~~~

The *core* tier provides basic functionalities and is conneted to various the third-party tools. The functionalities include:

- Retrieval (Elasticsearch)
- Storage (MongoDB key-value store)
- Machine learning (scikit-learn) 
- Evaluation (trec-eval).

Additionally, a separate data module is provided with functionality for loading and preprocessing standard data sets (DBpedia, Freebase, ClueWeb, etc.).

It is possible to connect additional external tools (or replace our default choices) by implementing standard interfaces of the respective core modules.

.. Note :: The core layer represents a versatile general-purpose modern IR library, which may also be accessed using command line tools.

Logic tier
~~~~~~~~~~~

The *logic* tier contains the main business logic, which is organized around five main modules: 

1. **Entity** provides access to the entity catalog (including knowledge bases and entity surface form dictionaries
2. **Query** provides the representation of search queries along with various preprocessing methods; 
3. **Features** is a collection of entity-related features, which may be used across different search tasks; 
4. **Entity retrieval (ER)** contains various entity ranking methods
5. **entity linking (EL)** implements entity linking functionality

The logic layer may not be accessed directly.


Services tier
~~~~~~~~~~~~~

The *services* tier provides end-user access to the toolkit’s functionality, throughout the command line, API, and web interface. Four main types of service is available: 

1. Entity retrieval (ER)
2. Entity linking (EL)
3. Target type identification (TTI)
4. Entity catalog (EC)

