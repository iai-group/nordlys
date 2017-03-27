RESTful API
===========

The following Nordlys services can be accessed through a RESTful API:

- :ref:`api_er`
- :ref:`api_el`
- :ref:`api_tti`
- :ref:`api_ec`

Below we describe the usage for each of the services.

The Nordlys endpoint URL is `http://api.nordlys.cc/ <http://api.nordlys.cc/>`_ .


.. _api_er:

Entity Retrieval
----------------

The service presents a ranked list of entities in response to an entity-bearing query.

Endpoint URI
~~~~~~~~~~~~
::

   http://api.nordlys.cc/er

Example
~~~~~~~

*Request:*

 http://api.nordlys.cc/er?q=total+recall&1st_num_docs=100&model=lm

*Response:*

.. code-block:: python

    {"query": "total recall",}
      "total_hits": 1000",
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
~~~~~~~~~~~

The following table lists the parameters needed in the request URL for entity retrieval.

+----------------+---------------------------------------------------------------+
|Parameters                                                                      |
+================+===============================================================+
|q *(required)*  | Search query                                                  |
+----------------+---------------------------------------------------------------+
|1st_num_docs    | The number of documents that will be re-ranked using a model. |
|                | The recommended value (esp. for baseline comparisons) is 1000.|
|                | Lower values, like 100, are recommended only when efficiency  |
|                | matters *(default: 1000)*.                                    |
+----------------+---------------------------------------------------------------+
|start           | Starting offset for ranked documents *(default:0)*.           |
+----------------+---------------------------------------------------------------+
|fields_return   | Comma-separated list of fields to return for each hit         |
|                | *(default: "")*.                                              |
+----------------+---------------------------------------------------------------+
|model           | Name of the retrieval model; Accepted values:                 |
|                | "bm25", "lm", "mlmprms"  *(default: "lm")*.                   |
|                |                                                               |
|                | * BM25: The BM25 model, as implemented in Elasticsearch.      |
|                |   This is the most efficient that is provided by Nordlys      |
|                |   (to this date).                                             |
|                |                                                               |
|                | * LM: Language Modeling [1] approach, which employs a single  |
|                |   a single  field representation of entities.                 |
|                |                                                               |
|                | * MLM: The Mixture of Language Models [2], which uses a linear|
|                |   combination of language models built for each field.        |
|                |                                                               |
|                | * PRMS: The Probabilistic Model for Semistructured Data [3],  |
|                |   which uses collection statistics to compute field weights in|
|                |   for MLM model.                                              |
+----------------+---------------------------------------------------------------+
|field           | The name of the field used for LM *(default: "catchall")*.    |
+----------------+---------------------------------------------------------------+
|fields          | Comma-separated list of the fields for PRMS                   |
|                | *(default: "catchall")*.                                      |
+----------------+---------------------------------------------------------------+
|field_weights   | Comma-separated list of fields and their corresponding        |
|                | weights for MLM (default: "catchall:1").                      |
+----------------+---------------------------------------------------------------+
|smoothing_method| Smoothing method for LM-based models; Accepted values:        |
|                | jm, dirichlet  *(default: "dirichlet")*.                      |
+----------------+---------------------------------------------------------------+
|smoothing_param | The value of smoothing parameters (lambda or mu); Accepted    |
|                | values: float, "avg_len"                                      |
|                | *(default for jm: 0.1, default for dirichlet: 2000)*.         |
+----------------+---------------------------------------------------------------+





.. _api_el:

Entity Linking in Queries
-------------------------

The service identifies entities in queries and links them to the corresponding entry in the Knowledge base (DBpedia).

Endpoint URI
~~~~~~~~~~~~~
::

   http://api.nordlys.cc/el

Example
~~~~~~~

- *Request:*
    http://api.nordlys.cc/el?q=total+recall+arnold
- *Response:*

  .. code-block:: python

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
~~~~~~~~~~
The following table lists the parameters needed in the request URL for entity linking.


+-----------------+------------------------------------------------------------+
|Parameters                                                                    |
+=================+============================================================+
| q *(required)*  | The search query                                           |
+-----------------+------------------------------------------------------------+
| method          | The name of method; Accepted values *(default: "cmns")*    |
|                 |                                                            |
|                 |  * CMNS: The baseline method that uses the overall.        |
|                 |    popularity of entities as link targets, implemented     |
|                 |    based on [5].                                           |
+-----------------+------------------------------------------------------------+
| threshold       | The entity linking threshold *(default for cmns: 0.1)*.    |
+-----------------+------------------------------------------------------------+




.. _api_tti:

Target Type Identification
--------------------------

The service assigns target types (or categories) to queries from the DBpedia type taxonomy.

Endpoint URI
~~~~~~~~~~~~~
::

   http://api.nordlys.cc/tti

Example
~~~~~~~

- *Request:*
   http://api.nordlys.cc/tti?q=obama
- *Response:*

  .. code-block:: python

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
~~~~~~~~~~~

The following table lists the parameters needed in the request URL for target type identification.

+-----------------+------------------------------------------------------------+
|Parameters                                                                    |
+=================+============================================================+
| q *(required)*  | The search query                                           |
+-----------------+------------------------------------------------------------+
| method          | The name of method; Accepted values: "tc", "ec",           |
|                 | *(default: "tc")*.                                         |
|                 |                                                            |
|                 |  * TC: The Type Centric (TC) method based on [6]. Both BM25|
|                 |    and LM can be used as a retrieval model here.           |
|                 |                                                            |
|                 |  * EC: The Entity Centric (EC) method, as described in [6],|
|                 |    based on [5].                                           |
+-----------------+------------------------------------------------------------+
| num_types       | The number of types to return.                             |
+-----------------+------------------------------------------------------------+
| start           | The starting offset for ranked types.                      |
+-----------------+------------------------------------------------------------+
| model           | Retrieval model, if method is "tc" or "ec";                |
|                 | Accepted values: "lm", "bm25".                             |
+-----------------+------------------------------------------------------------+




.. _api_ec:

Entity Catalog
--------------

This service is used for representing entities (with IDs, name variants, attributes, and relationships). Additionally, it provides statistics that can be utilized, among others, for result presentation (e.g., identifying prominent properties when generating entity cards).

Endpoint URI
~~~~~~~~~~~~~
::

   http://api.nordlys.cc/ec

Example
~~~~~~~

- *Request:*
   http://api.nordlys.cc/ec/<entity_id>
- *Response:*

  .. code-block:: python

    {
        "<dbo:abstract>": ["Albert Einstein was a German-born theoretical physicist ... ],
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
~~~~~~~~~~~

The following table lists the parameters needed in the request URL for entity catalog.

+-----------------+------------------------------------------------------------+
|Parameter                                                                     |
+=================+============================================================+
| entity id       | It is in the form of "<dbpedia:XXX>", where XXX denotes    |
|                 | the DBpedia/Wikipedia ID of an entity.                     |
+-----------------+------------------------------------------------------------+



References
----------

[1] Jay M Ponte and W Bruce Croft . 1998. *A Language modeling approach to information retrieval*. In Proc. of SIGIR '98. 275–281.

[2] Paul Ogilvie and Jamie Callan. 2003. *Combining document representations for known-item search*. Proc. of SIGIR '03 (2003), 143–150.

[3] Jinyoung Kim, Xiaobing Xue, and W Bruce Croft . 2009. *A probabilistic retrieval model for semistructured data*. In Proc. of ECIR '09. 228–239.

[4] Faegheh Hasibi, Krisztian Balog, and Svein Erik Bratsberg. 2016. *Exploiting entity linking in  queries for entity retrieval*. In Proc. of ICTIR ’16. 171–180.

[5] Faegheh Hasibi, Krisztian Balog, and Svein Erik Bratsberg. 2015. *Entity linking in  queries: Tasks and Evaluation*. In Proc. of ICTIR ’15. 171–180.

[6] Krisztian Balog, Robert Neumayer. 2012. *Hierarchical target type identification for entity-oriented queries*. In Proc. of CIKM '12. 2391–2394.
