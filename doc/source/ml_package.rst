Machine learning package
========================

This page describes how to make use of the :mod:`~nordlys.core.ml` package.


How to apply a machine learning model
-------------------------------------

Just run ::

		python -m nordlys.core.ml.ml <config_file>

where ``<config_file>`` is the path to the JSON configuration file.



How to make a configuration file
--------------------------------

A JSON configuration file (or simply config file) needs to specify the model and the data you will use.

Let's take a first look of a sample config file (available in ``data/ml_sample/config.json``) ::

    {
        "model": "gbrt",
        "category": "regression",
        "parameters":{
            "alpha": 0.1,
            "tree": 10,
            "depth": 5
        },
        "training_set": "data/ml_sample/train.json",
        "testing_set": "data/ml_sample/test.json",
        "save_model": "data/ml_sample/model.txt",
        "output_file": "data/ml_sample/output.json",
        "cross_validation":{
            "create_splits": true,
            "splits_file": "data/ml_sample/splits.json",
            "k": 5,
            "split_strategy": "q_id"}
        }
    }


The JSON must contain the following fields:

* ``model`` specifies which model to use;
* ``category`` is the particular category of that model;
* ``parameters`` holds the specific parameters for that model category.

Also, it must indicate the locations of your data:

* ``training_set``: the training dataset file;
* ``testing_set``: the testing dataset file;
* ``save_model``: the file where to save the model;
* ``output_file``:  the output file after successfully applying the model.


A note about evaluation
-----------------------

Let's look again at the sample config file ``data/ml_sample/config.json``.

An optional ``cross-validation`` field may be added to describe how to perform cross-validation. Its value is a dictionary wht its own fields:

* ``create_splits`` holds a Boolean flag. When set as ``true``, it always creates new splits. Otherwise, new splits will be created only if the provided ``split_file`` **does not exist**.
* ``splits_file`` indicates where to store the splits if they are required;
* ``k`` is the number of folds to use;
* ``split_strategy`` specifies which data property to use as splitting strategy.


(@TODO Also, for example, how to perform analysis of attribute importance)


How to set up your data
-----------------------

You need to describe your data to be used for training and testing.

You can look at an example of a *training data* file in ``data/ml_sample/train.json``. It is a JSON whose keys are each of the instance IDs. The respective value for a given instance is a dictionary, itself with 3 possible keys:

* ``properties`` is used to store ny other property of the instance. This allows to have simple instance IDs and at the same time to keep track of additional information about the instance. Example properties might be a query ID, or a query content.
* ``features`` specifies all the (attribute, value) pairs. It's important to note that **all the instances should specify the same set of features**.
* ``target`` indicates the target (or class, or label) for that instance.

The *testing data* is specified in the same way as the training data, excepting that its instance values do not contain a target.
