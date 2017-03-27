Machine leaning
===============

The command-line application for general-purpose machine learning.


Usage
-----

::

  python -m nordlys.core.ml.ml <config_file>


Config parameters
------------------

- **training_set**: nordlys ML instance file format (MIFF)
- **test_set**: nordlys ML instance file format (MIFF); if provided then it's always used for testing. Can be left empty if cross-validation is used, in which case the remaining split is used for testing.
- **cross_validation**:
   - k: number of folds (default: 10); use -1 for leave-one-out
   - split_strategy: name of a property (normally query-id for IR problems). If set, the entities with the same value for that property are kept in the same split. if not set, entities are randomly distributed among splits.
   - splits_file: JSON file with splits (instance_ids); if the file is provided it is used, otherwise it's generated
   - create_splits: if True, creates the CV splits. Otherwise loads the splits from "split_file" parameter.
- **model**: ML model, currently supported values: rf, gbrt
- **category**: [regression | classification], default: "regression"
- **parameters**: dict with parameters of the given ML model
   - If GBRT:
      - alpha: learning rate, default: 0.1
      - tree: number of trees, default: 1000
      - depth: max depth of trees, default: 10% of number of features
   - If RF:
      - tree: number of trees, default: 1000
      - maxfeat: max features of trees, default: 10% of number of features
- **save_model**: the model is saved to this file
- **load_model**: if True, loads the model
- **save_feature_imp**: Feature importance is saved to this file
- **output_file**: where output is written; default output format: TSV with with instance_id and (estimated) target


Example config
---------------

.. code:: python

	{
	    "model": "gbrt",
	    "category": "regression",
		"parameters":{
			"alpha": 0.1,
			"tree": 10,
			"depth": 5
		},
		"training_set": "path/to/train.json",
		"test_set": "path/to/test.json",
		"save_model": "path/to/model.txt",
	    "output_file": "path/to/output.json",
	    "cross_validation":{
			"create_splits": true,
			"splits_file": "path/to/splits.json",
	        "k": 5,
	        "split_strategy": "q_id"
		}
	}
