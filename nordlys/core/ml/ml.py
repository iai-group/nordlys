"""
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
- **model_file**: the model is saved to this file
- **load_model**: if True, loads the model
- **feature_imp_file**: Feature importance is saved to this file
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
		"model_file": "path/to/model.txt",
	    "output_file": "path/to/output.json",
	    "cross_validation":{
			"create_splits": true,
			"splits_file": "path/to/splits.json",
	        "k": 5,
	        "split_strategy": "q_id"
		}
	}

------------------------

:Authors: Faegheh Hasibi, Krisztian Balog
"""
import argparse
from sys import exit
import numpy
import pickle
from sklearn.ensemble import (GradientBoostingRegressor, GradientBoostingClassifier, RandomForestRegressor,
                              RandomForestClassifier)

from nordlys.core.ml.instances import Instances
from nordlys.core.ml.cross_validation import CrossValidation
from nordlys.config import PLOGGER
from nordlys.core.utils.file_utils import FileUtils


class ML(object):
    def __init__(self, config):
        self.__check_config(config)
        self.__config = config

    @staticmethod
    def __check_config(config):
        """Checks config parameters and set default values."""
        try:
            # if "training_set" not in config:
            #     raise Exception("training_set is missing")
            # if "output_file" not in config:
            #     raise Exception("output_file is missing")
            if "cross_validation" in config:
                if "splits_file" not in config["cross_validation"]:
                    raise Exception("splits_file is missing")
                if "k" not in config["cross_validation"]:
                    config["cross_validation"]["k"] = 10
            # else:
            #     if "test_set" not in config:
            #         raise Exception("test_set is missing")

        except Exception as e:
            PLOGGER.error("Error in config file: ", e)
            exit(1)

    def gen_model(self, num_features=None):
        """ Reads parameters and generates a model to be trained.

        :param num_features: int, number of features
        :return untrained ranker/classifier
        """
        model = None
        if self.__config["model"].lower() == "gbrt":
            alpha = self.__config["parameters"].get("alpha", 0.1)
            tree = self.__config["parameters"].get("tree", 1000)
            default_depth = round(num_features / 10.0) if num_features is not None else None
            depth = self.__config["parameters"].get("depth", default_depth)

            PLOGGER.info("Training instances using GBRT ...")
            PLOGGER.info("Number of trees: " + str(tree) + "\tDepth of trees: " + str(depth))
            if self.__config.get("category", "regression") == "regression":
                PLOGGER.info("Training regressor")
                model = GradientBoostingRegressor(n_estimators=tree, max_depth=depth, learning_rate=alpha)
            else:
                PLOGGER.info("Training the classifier")
                model = GradientBoostingClassifier(n_estimators=tree, max_depth=depth, learning_rate=alpha)

        elif self.__config["model"].lower() == "rf":
            tree = self.__config["parameters"].get("tree", 1000)
            default_maxfeat = round(num_features / 10.0) if num_features is not None else None
            max_feat = self.__config["parameters"].get("maxfeat", default_maxfeat)

            PLOGGER.info("Training instances using RF ...")
            PLOGGER.info("Number of trees: " + str(tree) + "\tMax features: " + str(max_feat))
            if self.__config.get("category", "regression") == "regression":
                PLOGGER.info("Training regressor")
                model = RandomForestRegressor(n_estimators=tree, max_features=max_feat)
            else:
                PLOGGER.info("Training classifier")
                model = RandomForestClassifier(n_estimators=tree, max_features=max_feat)
        return model

    def train_model(self, instances):
        """Trains model on a given set of instances.

        :param instances: Instances object
        :return: the learned model
        """

        features = instances.get_all()[0].features
        features_names = sorted(features.keys())
        PLOGGER.info("Number of instances:\t" + str(len(instances.get_all())))
        PLOGGER.info("Number of features:\t" + str(len(features_names)))
        # Converts instances to Scikit-learn format : (n_samples, n_features)
        n_samples = len(instances.get_all())
        train_x = numpy.zeros((n_samples, len(features_names)))
        train_y = numpy.empty(n_samples, dtype=object)  # numpy.zeros(n_samples)
        for i, ins in enumerate(instances.get_all()):
            train_x[i] = [ins.features[ftr] for ftr in features_names]
            if self.__config.get("category", "regression") == "regression":
                train_y[i] = float(ins.target)
            else:
                train_y[i] = str(ins.target)
        # training
        model = self.gen_model(len(features))
        model.fit(train_x, train_y)

        # write the trained model to the file
        if "model_file" in self.__config:
            # @todo if CV is used we need to append the fold no. to the filename
            PLOGGER.info("Writing trained model to {} ...".format(self.__config["model_file"]))
            pickle.dump(model, open(self.__config["model_file"], "wb"))

        if "feature_imp_file" in self.__config:
            print(self.analyse_features(model, features_names))
        return model

    def analyse_features(self, model, feature_names):
        """ Ranks features based on their importance.
        Scikit uses Gini score to get feature importances.

        :param model: trained model
        :param feature_names: list of feature names
        """

        # we sort the features to make sure that are in the same order as they used while training.
        # This is especially important when the function is called outside "train_model" function.
        feature_names = sorted(feature_names)

        # gets feature importance
        importances = zip(feature_names, model.feature_importances_)
        sorted_importances = sorted(importances, key=lambda imps: imps[1], reverse=True)

        feat_imp_str = "=========== Feature Importance ===========\n"
        for feat, importance in sorted_importances:
            feat_imp_str += feat + "\t" + str(importance) + "\n"
        feat_imp_str += "=========================================="
        open(self.__config["feature_imp_file"], "w").write(feat_imp_str)
        return feat_imp_str

    def apply_model(self, instances, model):
        """Applies model on a given set of instances.

        :param instances: Instances object
        :param model: trained model
        :return: Instances
        """
        PLOGGER.info("Applying model ... ")
        if len(instances.get_all()) > 0:
            features_names = sorted(instances.get_all()[0].features.keys())
            for ins in instances.get_all():
                test_x = numpy.array([[ins.features[ftr] for ftr in features_names]])
                if self.__config.get("category", "regression") == "regression":
                    ins.score = model.predict(test_x)[0]
                else:  # classification
                    ins.target = str(model.predict(test_x)[0])
                    # "predict_proba" gets class probabilities; an array of probabilities for each class e.g.[0.99, 0.1]
                    ins.score = model.predict_proba(test_x)[0][1]
        return instances

    def output(self, instances):
        """Writes results to output file.

        :param instances: Instances object
        """
        with open(self.__config["output_file"], "w") as f:
            f.write("id\tscore\n")  # output to file
            PLOGGER.info("id\ttarget\tscore\n")
            for ins in instances.get_all():
                f.write(ins.id + "\t" + "{0:.5f}".format(ins.score) + "\n")  # output to file
        PLOGGER.info("Output saved in: " + self.__config["output_file"])

    def run(self):
        # load training instances
        ins_train = Instances.from_json(self.__config["training_set"])

        # Cross Validation
        if "cross_validation" in self.__config:
            cv = CrossValidation(self.__config["cross_validation"]["k"], ins_train, self.train_model, self.apply_model)
            split_strategy = self.__config["cross_validation"].get("split_strategy", None)
            split_file = self.__config["cross_validation"]["splits_file"]
            # Always creates new splits if the create_flag is True
            if bool(self.__config["cross_validation"].get("create_splits", False)) is True:
                cv.create_folds(split_strategy)
                cv.save_folds(split_file)
            # New splits will be created only if the provided split_file does not exist.
            else:
                cv.get_folds(split_file, split_strategy)
            inss = cv.run()

        # classic test-train split
        else:
            ins_test = Instances.from_json(self.__config["test_set"])
            model = self.train_model(ins_train)
            inss = self.apply_model(ins_test, model)

        # output results (which are stored in inss)
        inss.to_json(self.__config["output_file"])
        # inss.to_treceval(self.__config["output_file"])
        # self.output(inss)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


def main(args):
    config = FileUtils.load_config(args.config)
    ml = ML(config)
    ml.run()


if __name__ == "__main__":
    main(arg_parser())

