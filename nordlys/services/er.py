"""
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
------------------------

:Author: Faegheh Hasibi

"""
import argparse
from pprint import pprint

from nordlys.config import ELASTIC_INDICES
from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.retrieval.retrieval import Retrieval
from nordlys.core.retrieval.scorer import Scorer
from nordlys.core.utils.file_utils import FileUtils

# Constants
DBPEDIA_INDEX = ELASTIC_INDICES[0]


class ER(object):
    def __init__(self, config, elastic=None):
        self.__check_config(config)
        self.__config = config
        self.__num_docs = int(config["num_docs"])
        self.__start = int(config["start"])
        self.__er = Retrieval(config)

        self.__elastic = elastic

    @staticmethod
    def __check_config(config):
        """Checks config parameters and set default values."""
        config["index_name"] = DBPEDIA_INDEX
        if config.get("first_pass", None) is None:
            config["first_pass"] = {}
        if config["first_pass"].get("1st_num_docs", None) is None:
            config["first_pass"]["1st_num_docs"] = 1000
        if config["first_pass"].get("fields_return", None) is None:
            config["first_pass"]["fields_return"] = ""
        if config.get("num_docs", None) is None:
            config["num_docs"] = config["first_pass"]["1st_num_docs"]
        if config.get("start", None) is None:
            config["start"] = 0
        if config.get("model", None) is None:
            config["model"] = "lm"
        # Todo: Check the ELR params
        return config

    def __get_scorer(self, query):
        """Factory method to get entity retrieval method."""
        scorer = Scorer.get_scorer(self.__elastic, query, self.__config)
        return scorer

    def retrieve(self, query):
        """Retrieves entities for a query"""
        scorer = self.__get_scorer(query)
        ens = self.__er.retrieve(query, scorer)

        # converts to output format
        res = {"query": query,
               "total_hits": len(ens),
               "results": {}}
        if len(ens) != 0:
            res["results"] = self.__get_top_k(ens)
        return res

    def __get_top_k(self, ens):
        """Returns top-k results."""
        sorted_ens = sorted(ens.items(), key=lambda item: item[1]["score"], reverse=True)
        results = {}
        end = min(self.__num_docs, len(ens))
        for i in range(self.__start, self.__start + end):
            en_id, en = sorted_ens[i][0], sorted_ens[i][1]
            results[i] = {"entity": en_id, "score": en["score"]}
            if en.get("fields", {}) != {}:
                results[i]["fields"] = en["fields"]
        return results


    def batch_retrieval(self):
        """Performs batch retrieval for a set of queries"""
        # todo: integrate ELR approach
        self.__er.batch_retrieval()


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="query string", type=str, default=None)
    parser.add_argument("-c", "--config", help="config file", type=str, default={})
    args = parser.parse_args()
    return args


def main(args):
    config = FileUtils.load_config(args.config)
    er = ER(config, ElasticCache(DBPEDIA_INDEX))

    if args.query:
        res = er.retrieve(args.query)
        pprint(res)
    else:
        er.batch_retrieval()

if __name__ == '__main__':
    main(arg_parser())