API Usage
=========

Nordlys services can be accessed through a RESTfull API. The services are:

- Entity Retrieval
- Entity Linking
- Target Type Identification
- Entity Catalog

Below we describe the usage for each of the services.

Nordlys endpoint URL is `http://api.nordlys.cc/ <http://api.nordlys.cc/>`_ .

1. Entity Retrieval (ER)
~~~~~~~~~~~~~~~~~~~~~~~~
The service presents a ranked list of entities in response to an entity-bearing query. 

Endpoint URI
^^^^^^^^^^^^
::

   http://api.nordlys.cc/er

Example
^^^^^^^

- *Request:* http://api.nordlys.cc/er?q=total+recall&model=lm

- *Response:*

  .. code-block::

    {
      "query": "total recall",
      "total_hits": 100", 
      "results": {
        "0": {
          "entity": "<dbpedia:Total_Recall_(1990_film)>", 
          "score": -10.042525028471253
        }, 
        "1": {
          "entity": "<dbpedia:Total_Recall_(2012_film)>", 
          "score": -10.295316626850521
        }, 
        ...
    }


Parameters
^^^^^^^^^^
Nordlys currently supports the following approaches for entity retrieval:

- **Elastic:**  The BM25 model, as implemented in Elasticsearch. This is the most efficient that is provided by nordlys (to this date).

- **LM:** Language Modeling [21] approach (with Dirichlet prior smoothing), which employs a single  eld representa- tion of entities.


2. Entity Linking in Queries (EL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The service identifies entities in queries and links them to the corresponding entry in the Knowledge base (DBpedia).

Endpoint URI
^^^^^^^^^^^^
::

   http://api.nordlys.cc/el

Example
^^^^^^^

- *Request:* http://api.nordlys.cc/el?q=total+recall+arnold

- *Response:*

  .. code-block::

    {
      "processed_query": "total recall arnold", 
      "query": "total recall arnold", 
      "results": {
        "recall arnold": [
          "<dbpedia:Arnold_Schwarzenegger>", 
          1.0
        ], 
        "total recall": [
          "<dbpedia:Total_Recall_(1990_film)>", 
          0.8167730173199635
        ]
      }
    }

Parameters
^^^^^^^^^^

3. Target Type Identification (TTI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The service assigns target types (or categories) to queries from DBpedia type taxonomy.

Endpoint URI
^^^^^^^^^^^^
::

   http://api.nordlys.cc/tti

Example
^^^^^^^

- *Request:* http://api.nordlys.cc/tti?q=obama

- *Response:*

  .. code-block::

    {
      "query": "obama", 
      "results": {
        "0": {
          "score": 3.3290777, 
          "type": "<dbo:Ambassador>"
        }, 
        "1": {
          "score": 3.2955842, 
          "type": "<dbo:Election>"
        }, 
        ...
    }

Parameters
^^^^^^^^^^


4. Entity Catalog (EC)
~~~~~~~~~~~~~~~~~~~~~~

This service is used for representing entities (with IDs, name variants, attributes, and relationships). Additionally, it provides statistics that can be utilized, among others, for result presentation (e.g., identifying prominent properties when generating entity cards).

Endpoint URI
^^^^^^^^^^^^
::

   http://api.nordlys.cc/ec

Example
^^^^^^^

- *Request:* http://api.nordlys.cc/ec/<dbpedia:Albert_Einstein>

- *Response:*

  .. code-block::

    {
        "<dbo:abstract>": ["Albert Einstein was a German-born theoretical physicist .. ],
        "<dbo:academicAdvisor>": ["<dbpedia:Heinrich_Friedrich_Weber>"],
        "<dbo:almaMater>": [
            "<dbpedia:ETH_Zurich>",
            "<dbpedia:University_of_Zurich>"
                           ],
        "<dbo:award>": [
            "<dbpedia:Nobel_Prize_in_Physics>",
            "<dbpedia:Max_Planck_Medal>",
            ...
                       ],
        "<dbo:birthDate>": ["1879-03-14"],
        ...
    }

Parameters
^^^^^^^^^^