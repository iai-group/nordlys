"""
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
"""

import argparse
import json
from pprint import pprint

import pickle

from nordlys.config import ELASTIC_INDICES, PLOGGER
from nordlys.core.ml.instances import Instances
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.utils.file_utils import FileUtils
from nordlys.logic.el.cmns import Cmns
from nordlys.logic.el.el_utils import load_kb_snapshot, to_elq_eval
from nordlys.logic.el.ltr import LTR
from nordlys.logic.entity.entity import Entity
from nordlys.logic.features.feature_cache import FeatureCache
from nordlys.logic.query.query import Query

# Constants
DBPEDIA_INDEX = ELASTIC_INDICES[0]


class EL(object):

    def __init__(self, config, entity, elastic=None, fcache=None):
        self.__check_config(config)
        self.__config = config
        self.__method = config["method"]
        self.__threshold = float(config["threshold"])
        self.__query_file = config.get("query_file", None)
        self.__output_file = config.get("output_file", None)

        self.__entity = entity
        self.__elastic = elastic
        self.__fcache = fcache
        self.__model = None
        if "kb_snapshot" in self.__config:
            load_kb_snapshot(self.__config["kb_snapshot"])

    @staticmethod
    def __check_config(config):
        """Checks config parameters and set default values."""
        if config.get("method", None) is None:
            config["method"] = "ltr"
        if config.get("step", None) is None:
            config["step"] = "linking"
        if config.get("threshold", None) is None:
            config["threshold"] = 0.1
        if config["method"] == "ltr":
            if config.get("model_file", None) is None:
                config["model_file"] = "data/el/model.txt"
        if config.get("kb_snapshot", None) is None:
            config["kb_snapshot"] = "data/el/snapshot_2015_10.txt"
        return config

    def __get_linker(self, query):
        """Returns the entity linker based on the given model and parameters

        :param query: query object
        :return: entity linking object
        """
        if self.__method.lower() == "cmns":
            return Cmns(query, self.__entity, threshold=self.__threshold)
        if self.__method.lower() == "ltr":
            if self.__model is None:
                self.__model = pickle.load(open(self.__config["model_file"], "rb"))
            return LTR(query, self.__entity, self.__elastic, self.__fcache, self.__model, threshold=self.__threshold)
        else:
            raise Exception("Unknown model " + self.__method)

    def link(self, query, qid=""):
        """Performs entity linking for the query.

        :param query: query string
        :return: annotated query
        """
        PLOGGER.info("Linking query " + qid + " [" + query + "] ")
        q = Query(query, qid)
        linker = self.__get_linker(q)
        if self.__config["step"] == "ranking":
            res = linker.rank_ens()
        else:
            linked_ens = linker.link()
            res = {"query": q.raw_query,
                   "processed_query": q.query,
                   "results": linked_ens}
        return res

    def batch_linking(self):
        """Scores queries in a batch and outputs results."""
        results = {}

        if self.__config["step"] == "linking":
            queries = json.load(open(self.__query_file))
            for qid in sorted(queries):
                results[qid] = self.link(queries[qid], qid)
            to_elq_eval(results, self.__output_file)
            # json.dump(results, open(self.__output_file, "w"), indent=4, sort_keys=True)

        # only ranking step
        if self.__config["step"] == "ranking":
            queries = json.load(open(self.__query_file))
            for qid in sorted(queries):
                linker = self.__get_linker(Query(queries[qid], qid))
                results[qid] = linker.rank_ens()
            ranked_inss = Instances(sum([inss.get_all() for inss in results.values()], []))
            ranked_inss.to_treceval(self.__output_file)
            if self.__config.get("json_file", None):
                ranked_inss.to_json(self.__config["json_file"])

        # only disambiguation step
        if self.__config["step"] == "disambiguation":
            inss = Instances.from_json(self.__config["test_set"])
            inss_by_query = inss.group_by_property("qid")
            for qid, q_inss in sorted(inss_by_query.items()):
                linker = self.__get_linker("")
                results[qid] = {"results": linker.disambiguate(Instances(q_inss))}
            if self.__config.get("json_file", None):
                json.dump(open(self.__config["json_file"], "w"), results, indent=4, sort_keys=True)
            to_elq_eval(results, self.__output_file)

        PLOGGER.info("Output file: " + self.__output_file)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="query string", type=str, default=None)
    parser.add_argument("-c", "--config", help="config file", type=str, default={})
    args = parser.parse_args()
    return args


def main(args):
    conf = FileUtils.load_config(args.config)
    el = EL(conf, Entity(), ElasticCache(DBPEDIA_INDEX), FeatureCache())

    if conf.get("gen_model", False):
        LTR.train(conf)
    if args.query:
        res = el.link(args.query)
        pprint(res)
    else:
        el.batch_linking()

if __name__ == '__main__':
    main(arg_parser())

