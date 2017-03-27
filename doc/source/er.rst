Entity Retrieval
================

Command-line application for entity retrieval.

Usage
-----

::

  python -m nordlys.services.er -c <config_file> -q <query>

If `-q <query>` is passed, it returns the results for the specified query and prints them in terminal.


Config parameters
------------------

- **index_name**: name of the index,
- **first_pass**:
      - **num_docs**: number of documents in first-pass scoring (default: 100)
      - **field**: field used in first pass retrieval (default: Elastic.FIELD_CATCHALL)
      - **fields_return**: comma-separated list of fields to return for each hit (default: "")
- **num_docs**: number of documents to return (default: 100)
- **start**: starting offset for ranked documents (default:0)
- **model**: name of retrieval model; accepted values: [lm, mlm, prms] (default: lm)
- **field**: field name for LM (default: catchall)
- **fields**: list of fields for PRMS (default: [catchall])
- **field_weights**: dictionary with fields and corresponding weights for MLM (default: {catchall: 1})
- **smoothing_method**: accepted values: [jm, dirichlet] (default: dirichlet)
- **smoothing_param**: value of lambda or mu; accepted values: [float or "avg_len"], (jm default: 0.1, dirichlet default: 2000)
- **query_file**: name of query file (JSON),
- **output_file**: name of output file,
- **run_id**: run id for TREC output


Example config
---------------

.. code:: python

	{"index_name": "dbpedia_2015_10",
	  "first_pass": {
	    "num_docs": 1000
	  },
	  "model": "prms",
	  "num_docs": 1000,
	  "smoothing_method": "dirichlet",
	  "smoothing_param": 2000,
	  "fields": ["names", "categories", "attributes", "similar_entity_names", "related_entity_names"],
	  "query_file": "path/to/queries.json",
	  "output_file": "path/to/output.txt",
	  "run_id": "test"
	}