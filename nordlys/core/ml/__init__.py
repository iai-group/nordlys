"""
Machine learning
================

The machine learning package is connected to `Scikit-learn <http://scikit-learn.org/stable/>`_ and can be used for learning-to-rank and classification purposes.


Usage
-----

For information on how to use the package from command line and set the configuration, read :doc:`ML usage <api/nordlys.core.ml.ml>`



Data format
-----------

The file format of the training and test files is `json`. Each instance is presented as a dictionary, consist of the following elements:

- **ID**: Instance id
- **Target**: The target value of the instance.
- **Features**: All the features, presented in key-value format. Note that all the instances should have the same set of features.
- **Properties**: All meta-data about the instance; e.g. query ID, or content.

Below is an excerpt from a json data file:

.. code:: python

    {
        "0": {
            "properties": {
                "query": "papaqui soccer",
                "entity": "<dbpedia:Soccer_(1985_video_game)>"
            },
            "target": "0",
            "features": {
                "feat1": 1,
                "feat2": 0,
                "feat3": 25
            }
        },
        "1": {}
    }

.. note :: The sample files for using the ML package are provided under ``data/ml_sample/`` folder.

.. note :: Currently we provide support for Random Forest(RF) and Gradient Boosted Regression Trees (GBRT).

"""