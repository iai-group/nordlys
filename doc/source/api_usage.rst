API usage
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
^^^^^^^^^^

- **q** *(required)* is the search query
- **1st_num_docs** is the number of documents that will be re-ranked using a model. The recommended value (esp. for baseline comparisons) is 1000. Lower values, like 100, are recommended only when efficiency matters *(default: 1000)*
- **num_docs** is the total number of documents (entities) to return *(default: 100)*
- **start** is starting offset for ranked documents *(default:0)*
- **fields_return** is comma-separated list of fields to return for each hit *(default: "")*
- **model** is name of the retrieval model; accepted values: [bm25 | lm | mlm | prms] *(default: "lm")* 
   - **BM25**: The BM25 model, as implemented in Elasticsearch. This is the most efficient that is provided by Nordlys (to this date)
   - **LM**: Language Modeling [1] approach, which employs a single  field representation of entities
   - **MLM**: The Mixture of Language Models [2], which uses a linear combination of language models built for each field
   - **PRMS**: The Probabilistic Model for Semistructured Data [3], which uses collection statistics to compute field weights in for MLM model
- **field** is name of the field used for LM *(default: "catchall")*
- **fields** is comma-separated list of the fields for PRMS *(default: "catchall")*
- **field_weights** is comma-separated list of fields and their corresponding weights for MLM (default: "catchall:1")
- **smoothing_method** is smoothing method for LM-based models; accepted values: jm|dirichlet *(default: "dirichlet")*
- **smoothing_param** is the value of smoothing parameters (lambda or mu); accepted values: [float or "avg_len"] *(default for jm: 0.1, default for dirichlet: 2000)*


2. Entity Linking in Queries (EL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The service identifies entities in queries and links them to the corresponding entry in the Knowledge base (DBpedia).

Endpoint URI
^^^^^^^^^^^^
::

   http://api.nordlys.cc/el

Example
^^^^^^^

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
^^^^^^^^^^

- **q** *(required)* is the search query
- **method** is the name of the method; accepted values *(default: "cmns")*
   - **CMNS**  The baseline method that uses the overall popularity of entities as link targets, implemented based on [5]
- **threshold** is the entity linking threshold *(default for cmns: 0.1)*


3. Target Type Identification (TTI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The service assigns target types (or categories) to queries from DBpedia type taxonomy.

Endpoint URI
^^^^^^^^^^^^
::

   http://api.nordlys.cc/tti

Example
^^^^^^^

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
^^^^^^^^^^

- **q** *(required)* is the search query
- **method** is the name of the method; accepted values: [tc | ec], *(default: "tc")*
  - **TC**: The Type Centric (TC) method based on [6]. Both BM25 and LM can be used as a retrieval model here.
  - **EC**: The Entity Centric (EC) method, as described in [6].
- **num_types** is the number of types to return,
- **start** is the starting offset for ranked types,
- **model** is retrieval model, if method is "tc" or "ec"; accepted values: [lm |bm25],

4. Entity Catalog (EC)
~~~~~~~~~~~~~~~~~~~~~~

This service is used for representing entities (with IDs, name variants, attributes, and relationships). Additionally, it provides statistics that can be utilized, among others, for result presentation (e.g., identifying prominent properties when generating entity cards).

Endpoint URI
^^^^^^^^^^^^
::

   http://api.nordlys.cc/ec

Example
^^^^^^^

- *Request:* 
   http://api.nordlys.cc/ec/<dbpedia:Albert_Einstein>
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
^^^^^^^^^^

- Entity id in the form of "<dbpedia:XXX>", where XXX denotes the DBpedia/Wikipedia ID of an entity

References
~~~~~~~~~~

[1] Jay M Ponte and W Bruce Croft . 1998. *A Language modeling approach to information retrieval*. In Proc. of SIGIR '98. 275–281.

[2] Paul Ogilvie and Jamie Callan. 2003. *Combining document representations for known-item search*. Proc. of SIGIR '03 (2003), 143–150.

[3] Jinyoung Kim, Xiaobing Xue, and W Bruce Croft . 2009. *A probabilistic retrieval model for semistructured data*. In Proc. of ECIR '09. 228–239.

[4] Faegheh Hasibi, Krisztian Balog, and Svein Erik Bratsberg. 2016. *Exploiting entity linking in  queries for entity retrieval*. In Proc. of ICTIR ’16. 171–180.

[5] Faegheh Hasibi, Krisztian Balog, and Svein Erik Bratsberg. 2015. *Entity linking in  queries: Tasks and Evaluation*. In Proc. of ICTIR ’15. 171–180.

[6] Krisztian Balog, Robert Neumayer. 2012. *Hierarchical target type identification for entity-oriented queries*. In Proc. of CIKM '12. 2391–2394.