Nordlys architecture
====================

Nordlys is based on a `multitier architecture <https://en.wikipedia.org/wiki/Multitier_architecture>`_ with three layers:

  - :doc:`core <api/nordlys.core>` (data tier)
  - :doc:`logic <api/nordlys.logic>`
  - :doc:`services <api/nordlys.services>` (presentation tier)

.. figure::  figures/nordlys_architecture-basic.png
   :align:   center

   Nordlys architecture.




Core tier
~~~~~~~~~~~

The *core* tier provides basic functionalities and is conneted to various the third-party tools. The functionalities include:

- :doc:`Retrieval <api/nordlys.core.retrieval>` (based on `Elasticsearch <https://www.elastic.co/>`_)
- :doc:`Storage <api/nordlys.core.storage>` (based on `MongoDB <https://www.mongodb.com/>`_)
- :doc:`Machine learning <api/nordlys.core.ml>` (based on `scikit-learn <http://scikit-learn.org/>`_)
- :doc:`Evaluation <api/nordlys.core.eval>` (based on `trec-eval <https://github.com/usnistgov/trec_eval>`_)

Additionally, a separate :doc:`data <api/nordlys.core.data>` package is provided with functionality for loading and preprocessing standard data sets (DBpedia, Freebase, ClueWeb, etc.).

It is possible to connect additional external tools (or replace our default choices) by implementing standard interfaces of the respective core modules.

.. Note :: The core layer represents a versatile general-purpose modern IR library, which may also be accessed using command line tools.

Logic tier
~~~~~~~~~~~

The *logic* tier contains the main business logic, which is organized around five main modules:

1. :doc:`Entity <api/nordlys.logic.entity>` provides access to the entity catalog (including knowledge bases and entity surface form dictionaries.
2. :doc:`Query <api/nordlys.logic.query>` provides the representation of search queries along with various preprocessing methods.
3. :doc:`Features <api/nordlys.logic.features>` is a collection of entity-related features, which may be used across different search tasks.
4. :doc:`Entity retrieval <api/nordlys.logic.er>` contains various entity ranking methods.
5. :doc:`Entity linking <api/nordlys.logic.el>` implements entity linking functionality.

The logic layer may not be accessed directly (i.e.,as a service or as a command line application).


Services tier
~~~~~~~~~~~~~

The *services* tier provides end-user access to the toolkit’s functionality, throughout the :doc:`command line <cmd_usage>`, :doc:`API <restful_api>`, and :doc:`web interface <web_gui>`. Four main types of service is available:

1. :doc:`Entity retrieval <api/nordlys.services.er>`
2. :doc:`Entity linking <api/nordlys.services.el>`
3. :doc:`Target type identification <api/nordlys.services.tti>`
4. :doc:`Entity catalog <api/nordlys.services.ec>`
