Entity Linking (EL)
====================

The command-line endpoint for entity linking

Usage
-----

::

  python -m nordlys.services.er -c <config_file> -q <query>

If `-q <query>` is passed, it returns the resutls for the specified query and prints them in terminal.

Config parameters
-----------------

- **method**: name of the method
    - **CMNS**  The baseline method that uses the overall popularity of entities as link targets
- **threshold**: entity linking threshold; varies depending on the method *(default for cmns: 0.1)*
- **query_file**: name of query file (JSON)
- **output_file**: name of output file

Example config
---------------

.. code:: python

	{
	  "method": "cmns",
	  "threshold": 0.1,
	  "query_file": "path/to/queries.json"
	  "output_file": "path/to/output.json"
	}
