Nordlys |release| documentation
===============================



Nordlys is a toolkit for entity-oriented and semantic search, created by the IAI group at the University of Stavanger.


Entities (such as people, organizations, or products) are meaningful units for organizing information and can provide direct answers to many search queries. Nordlys is a toolkit for entity-oriented and semantic search.

Nordlys supports 3 functionalities in the context of entity-oriented search:

- :doc:`Entity retrieval <er>`: Returns a ranked list of entities in response to a query
- :doc:`Entity linking <el>`: Identifies entities in a query and links them to the corresponding entry in the Knowledge base
- :doc:`Target type identification <tti>`:  Detects the target types (or categories) of a query

Check our :doc:`Web interface documentation <web_gui>` for illustration of each of these functionalities.


Nordlys can be used ...
------------------------

- through a :doc:`web-based GUI <web_gui>`
- through a :doc:`RESTful API <restful_api>`
- as a :doc:`command line tool <cmd_usage>`
- as a :doc:`Python package <api/nordlys>`


Contents
========

.. toctree::
   :maxdepth: 1

   installation
   data
   restful_api
   web_gui
   cmd_usage
   architecture
   Python package documentation <api/nordlys>
   contact


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
