Target Type Identification
==========================

The command-line application for target type indentification.

Usage
-----

::

  python -m nordlys.services.er <config_file> -q <query>

If `-q <query>` is passed, it returns the resutls for the specified query and prints them in terminal.

Config parameters
------------------

- **method**: name of TTI method; accepted values: ["tc", "ec"]
- **num_docs**: number of documents to return
- **start**: starting offset for ranked documents
- **model**: retrieval model, if method is "tc" or "ec"; accepted values: ["lm", "bm25"]
- **index**: if method is "tc", name of the index
- **ec_k_cutoff**: if method is "ec", rank cut-off of top-K entities for EC TTI
- **field**: field name for LM model, if method is "tc" or "ec"
- **smoothing_method**: accepted values: ["jm", "dirichlet"]
- **smoothing_param**: value of lambda or mu; accepted values: [float or "avg_len"]
- **query_file**: name of query file (JSON)
- **output_file**: name of output file


Example config
---------------

.. code:: python

	{"method": "tc",
	 "num_docs": 1000,
     "model" : "lm",
	  "smoothing_method": "dirichlet",
	  "smoothing_param": 2000,
	  "query_file": "path/to/queries.json",
	  "output_file": "path/to/output.txt",
	}
