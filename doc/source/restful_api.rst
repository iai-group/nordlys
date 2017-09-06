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

**Request:**

 http://api.nordlys.cc/er?q=total+recall&1st_num_docs=100&model=lm

**Response:**

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
~~~~~~~~~~

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
|                | weights for MLM *(default: "catchall:1")*.                    |
+----------------+---------------------------------------------------------------+
|smoothing_method| Smoothing method for LM-based models; Accepted values:        |
|                | jm, dirichlet  *(default: "dirichlet")*.                      |
+----------------+---------------------------------------------------------------+
|smoothing_param | The value of smoothing parameters (lambda or mu); Accepted    |
|                | values: float, "avg_len"                                      |
|                | *(default for "jm": 0.1, default for "dirichlet": 2000)*.     |
+----------------+---------------------------------------------------------------+





.. _api_el:

Entity Linking in Queries
-------------------------

The service identifies entities in queries and links them to the corresponding entry in the Knowledge base (DBpedia).

Endpoint URI
~~~~~~~~~~~~
::

   http://api.nordlys.cc/el

Example
~~~~~~~

- **Request:**
    http://api.nordlys.cc/el?q=total+recall
- **Response:**

  .. code-block:: python

	{
	  "processed_query": "total recall", 
	  "query": "total recall", 
	  "results": [
	    {
	      "entity": "<dbpedia:Total_Recall_(1990_film)>", 
	      "mention": "total recall", 
	      "score": 0.4013333333333334
	    }, 
	    {
	      "entity": "<dbpedia:Total_Recall_(2012_film)>", 
	      "mention": "total recall", 
	      "score": 0.315
	    }
	  ]
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
|                 |  * cmns: The baseline method that uses the overall.        |
|                 |    popularity of entities as link targets, implemented     |
|                 |    based on [5].                                           | 
|                 |                                                            | 
|                 |  * ltr: The learning-to-rank model, implemented based on   |
|                 |    the LTR-greedy in [9]. Note that the implemented method |
|                 |    is slightly different from [9] (due to efficiency       |
|                 |    reasons).                                               |
+-----------------+------------------------------------------------------------+
| threshold       | The entity linking threshold *(default: 0.1)*.             |
+-----------------+------------------------------------------------------------+




.. _api_tti:

Target Type Identification
--------------------------

The service assigns target types (or categories) to queries from the DBpedia type taxonomy.

Endpoint URI
~~~~~~~~~~~~
::

   http://api.nordlys.cc/tti

Example
~~~~~~~

- **Request:**
    http://api.nordlys.cc/tti?q=obama

- **Response:**

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
~~~~~~~~~~

The following table lists the parameters needed in the request URL for target type identification.

+-----------------+------------------------------------------------------------+
|Parameters                                                                    |
+=================+============================================================+
| q *(required)*  | The search query                                           |
+-----------------+------------------------------------------------------------+
| method          | The name of method; accepted values: "tc", "ec", "ltr"     |
|                 | *(default: "tc")*.                                         |
|                 |                                                            |
|                 |  * TC: The Type Centric (TC) method based on [6]. Both BM25|
|                 |    and LM models can be used as a retrieval model here.    |
|                 |    This method fits the early fusion design pattern in [7].|
|                 |                                                            |
|                 |  * EC: The Entity Centric (EC) method, as described in [6].|
|                 |    Both BM25 and LM models can be used as a retrieval model|
|                 |    here. This method fits the late fusion design pattern in|
|                 |    [7].                                                    |
|                 |                                                            |
|                 |  * LTR: The Learing-To-Rank (LTR) method, as proposed in   |
|                 |    [8].                                                    |
+-----------------+------------------------------------------------------------+
| num_docs        | The number of top ranked target types to retrieve          |
|                 | *(default: 10)*.                                           |
+-----------------+------------------------------------------------------------+
| start           | The starting offset for ranked types.                      |
+-----------------+------------------------------------------------------------+
| model           | Retrieval model, if method is "tc" or "ec";                |
|                 | Accepted values: "lm", "bm25".                             |
+-----------------+------------------------------------------------------------+
| ec_cutoff       | If method is "ec", rank cut-off of top-K entities for EC   |
|                 | TTI.                                                       |
+-----------------+------------------------------------------------------------+
| field           | Field name, if method is "tc" or "ec".                     |
+-----------------+------------------------------------------------------------+
| smoothing_method| If model is "lm", smoothing method; accepted values: "jm", |
|                 | "dirichlet".                                               |
+-----------------+------------------------------------------------------------+
| Smoothing_param | If model is "lm", smoothing parameter; accepted values:    |
|                 | float, "avg_len".                                          |
+-----------------+------------------------------------------------------------+




.. _api_ec:

Entity Catalog
--------------

This service is used for representing entities (with IDs, name variants, attributes, and relationships). Additionally, it provides statistics that can be utilized, among others, for result presentation (e.g., identifying prominent properties when generating entity cards).

Endpoint URI
~~~~~~~~~~~~
::

   http://api.nordlys.cc/ec

Look up entity by ID
~~~~~~~~~~~~~~~~~~~~

- **Request:**

  ::

    http://api.nordlys.cc/ec/lookup_id/<entity_id>

- **Example:**

    http://api.nordlys.cc/ec/lookup_id/<dbpedia:Albert_Einstein>

- **Response:**

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



Look up entity by name (DBpedia)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Looks up an entity by its surface form in DBpedia.

- **Request:**

  ::

    http://api.nordlys.cc/ec/lookup_sf/dbpedia/<sf>

- **Example:**

   http://api.nordlys.cc/ec/lookup_sf/dbpedia/new%20york

- **Response:**

  .. code-block:: python

    {
        "_id": "new york"
        "<rdfs:label>" : {
          "<dbpedia:New_York>": 1
        }
        "<dbo:wikiPageDisambiguates>": {
          "<dbpedia:Manhattan>": 1,
          "<dbpedia:New_York,_Kentucky>": 1,
          ...
        }
        ...
    }

Look up entity by name (FACC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Looks up an entity by its surface form in FACC.

- **Request:**

  ::

    http://api.nordlys.cc/ec/lookup_sf/facc/<sf>

- **Example:**

    http://api.nordlys.cc/ec/lookup_sf/facc/new%20york

- **Response:**

  .. code-block:: python

    {
        "_id" : "new york",
        "facc12" : {
          "<fb:m.02_286>": 18706787,
          "<fb:m.02_53fb>": 49,
          "<fb:m.02_b9l>": 87,
          "<fb:m.02_l43>": 12,
          "<fb:m.02_l5n>": 23963,
          ...
        }
    }


Map Freebase entity ID to DBpedia ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Request:**

  ::

    http://api.nordlys.cc/ec/freebase2dbpedia/<fb_id>

- **Example:**

    http://api.nordlys.cc/ec/freebase2dbpedia/<fb:m.02_286>

- **Response:**

  .. code-block:: python

    {
      "dbpedia_ids": [
        "<dbpedia:New_York_City>"
      ]
    }


Map DBpedia entity ID to Freebase ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Request:**

  ::

    http://api.nordlys.cc/ec/dbpedia2freebase/<dbp_id>

- **Example:**

     http://api.nordlys.cc/ec/dbpedia2freebase/<dbpedia:New_York>


- **Response:**

  .. code-block:: python

    {
      "freebase_ids": [
        "<fb:m.059rby>"
      ]
    }

Parameters
~~~~~~~~~~

The following table lists the parameters needed in the request URL for entity catalog.

+-----------------+------------------------------------------------------------+
|Parameter                                                                     |
+=================+============================================================+
| entity id       | It is in the form of "<dbpedia:XXX>", where XXX denotes    |
|                 | the DBpedia/Wikipedia ID of an entity.                     |
+-----------------+------------------------------------------------------------+
| sf              | Entity surface form (e.g., "john smith", "new york").      |
|                 | It needs to be url-escaped.                                |
+-----------------+------------------------------------------------------------+
| fb_id           | Freebase ID                                                |
+-----------------+------------------------------------------------------------+
| bdp_id          | DBpedia ID                                                 |
+-----------------+------------------------------------------------------------+

References
----------

[1] Jay M Ponte and W Bruce Croft . 1998. *A Language modeling approach to information retrieval*. In Proc. of SIGIR '98. 275–281.

[2] Paul Ogilvie and Jamie Callan. 2003. *Combining document representations for known-item search*. Proc. of SIGIR '03 (2003), 143–150.

[3] Jinyoung Kim, Xiaobing Xue, and W Bruce Croft . 2009. *A probabilistic retrieval model for semistructured data*. In Proc. of ECIR '09. 228–239.

[4] Faegheh Hasibi, Krisztian Balog, and Svein Erik Bratsberg. 2016. *Exploiting entity linking in  queries for entity retrieval*. In Proc. of ICTIR ’16. 171–180. `[BIB] <http://krisztianbalog.com/showpub.php?id=Hasibi:2016:EEL>`_ `[PDF] <http://krisztianbalog.com/files/ictir2016-elr.pdf>`_

[5] Faegheh Hasibi, Krisztian Balog, and Svein Erik Bratsberg. 2015. *Entity linking in  queries: Tasks and Evaluation*. In Proc. of ICTIR ’15. 171–180. `[BIB] <http://krisztianbalog.com/showpub.php?id=Hasibi:2015:ELQ>`_ `[PDF] <http://krisztianbalog.com/files/ictir2015-erd.pdf>`_

[6] Krisztian Balog, Robert Neumayer. 2012. *Hierarchical target type identification for entity-oriented queries*. In Proc. of CIKM '12. 2391–2394. `[BIB] <http://krisztianbalog.com/showpub.php?id=Balog:2012:HTT>`_ `[PDF] <http://krisztianbalog.com/files/cikm2012-querytypes.pdf>`_

[7] Shuo Zhang and Krisztian Balog. *Design Patterns for Fusion-Based Object Retrieval*. In Proc. of ECIR '17. 684-690. `[BIB] <http://krisztianbalog.com/showpub.php?id=Zhang:2017:DPF>`_ `[PDF] <http://krisztianbalog.com/files/ecir2017-fusion.pdf>`_

[8] Darío Garigliotti, Faegheh Hasibi, and Krisztian Balog. *Target Type Identification for Entity-Bearing Queries*. In Proc. of SIGIR '17. `[BIB] <http://krisztianbalog.com/showpub.php?id=Garigliotti:2017:TTI>`_ `[PDF] <http://krisztianbalog.com/files/sigir2017-qt.pdf>`_

[9] Faegheh Hasibi, Krisztian Balog, and Svein Erik Bratsberg. 2017. *Entity linking in  queries: Efficiency vs. Effectiveness*. In Proc. of ECIR ’17. 40-53. `[BIB] <http://krisztianbalog.com/showpub.php?id=Hasibi:2017:ELQ>`_ `[PDF] <http://krisztianbalog.com/files/ecir2017-erd.pdf>`_

