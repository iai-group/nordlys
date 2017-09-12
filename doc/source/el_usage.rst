Entity Linking
==============

The command-line application for entity linking

Usage
-----

::

  python -m nordlys.services.el -c <config_file> -q <query>

If `-q <query>` is passed, it returns the results for the specified query and prints them in terminal.

Config parameters
-----------------

- **method**: name of the method
    - **cmns**  The baseline method that uses the overall popularity of entities as link targets
    - **ltr** The learning-to-rank model
- **threshold**: Entity linking threshold; varies depending on the method *(default: 0.1)*
- **step**: The step of entity linking process: [linking|ranking|disambiguation], *(default: linking)*
- **kb_snapshot**: File containing the KB snapshot of proper named entities; required for LTR, and optional for CMNS
- **query_file**: name of query file (JSON)
- **output_file**: name of output file

*Parameters of LTR method:*

- **model_file**: The trained model file; *(default:"data/el/model.txt")*
- **ground_truth**: The ground truth file; *(optional)*
- **gen_training_set**: If True, generates the training set from the groundtruth and query files; *(default: False)*
- **gen_model**: If True, trains the model from the training set; *(default: False)*
- The other parameters are similar to the nordlys.core.ml.ml settings


Example config
---------------

.. code:: python

	{
	  "method": "cmns",
	  "threshold": 0.1,
	  "query_file": "path/to/queries.json"
	  "output_file": "path/to/output.json"
	}

------------------------

:Author: Faegheh Hasibi