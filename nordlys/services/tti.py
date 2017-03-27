"""
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
------------------------

:Author: Dario Garigliotti
"""

from os.path import expanduser
import argparse
import json
from pprint import pprint

from nordlys.config import ELASTIC_TTI_INDICES
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.utils.file_utils import FileUtils
from nordlys.core.retrieval.retrieval import Retrieval
from nordlys.core.retrieval.scorer import Scorer

TTI_METHOD_TC = "tc"
TTI_METHOD_EC = "ec"
TTI_MODEL_BM25 = "bm25"
TTI_MODEL_LM = "lm"

DEFAULT_1ST_PASS_NUM_DOCS = 50  # Efficiency-related setting; it should be enough for types
DEFAULT_1ST_PASS_FIELD = "content"

DEFAULT_TTI_METHOD = TTI_METHOD_TC
DEFAULT_TTI_NUM_DOCS = 10  # enough for displaying top types
DEFAULT_TTI_START = 0
DEFAULT_TTI_TC_INDEX = ELASTIC_TTI_INDICES[0]
DEFAULT_TTI_EC_K_CUTOFF = 20  # Known to be a sufficient cut-off


class TTI(object):
    def __init__(self, config):
        self.__check_config(config)
        self.__config = config
        self.__method = config["method"]
        self.__num_docs = config["num_docs"]
        self.__start = config["start"]
        self.__tc_config = {
            "index_name": self.__config["index"],
            "first_pass": {
                "num_docs": DEFAULT_1ST_PASS_NUM_DOCS,
                "field": DEFAULT_1ST_PASS_FIELD
            },
        }
        self.__query_file = config.get("query_file", None)
        self.__output_file = config.get("output_file", None)

    @staticmethod
    def __check_config(config):
        """Checks config parameters and set default values."""
        config["method"] = config.get("method", TTI_METHOD_TC)
        config["num_docs"] = int(config.get("num_docs", DEFAULT_TTI_NUM_DOCS))
        config["start"] = int(config.get("start", DEFAULT_TTI_START))
        config["index"] = config.get("index", DEFAULT_TTI_TC_INDEX)

        return config

    def __entity_centric(self, query):
        """Entity-centric TTI."""
        types = dict()

        # ---
        # TODO
        ec_k_cutoff = self.__config.get("ec_k_cutoff", DEFAULT_TTI_EC_K_CUTOFF)
        # ... TODO
        # ---

        return types

    def __type_centric(self, query):
        """Type-centric TTI."""
        types = dict()
        model = self.__config.get("model", TTI_MODEL_BM25)

        elastic = ElasticCache(self.__tc_config.get("index", DEFAULT_TTI_TC_INDEX))
        if model == TTI_MODEL_BM25:
            print("TTI, TC, BM25")
            scorer = Scorer.get_scorer(elastic, query, self.__tc_config)
            types = Retrieval(self.__tc_config).retrieve(query, scorer)

        elif model == TTI_MODEL_LM:
            print("TTI, TC, LM")
            self.__tc_config["model"] = "lm"  # Needed for 2nd-pass
            self.__tc_config["field"] = "content"  # Needed for 2nd-pass
            self.__tc_config["second_pass"] = {
                "field": "content"
            }
            for param in ["smoothing_method", "smoothing_param"]:
                if self.__config.get(param, None) is not None:
                    self.__tc_config["second_pass"][param] = self.__config.get(param)

            scorer = Scorer.get_scorer(elastic, query, self.__tc_config)
            types = Retrieval(self.__tc_config).retrieve(query, scorer)

        return types

    def identify(self, query):
        """Performs target type identification for the query.

        :param query: query string
        :return: annotated query
        """
        # obtains types according to requested method
        method = self.__config.get("method", None)
        if method == TTI_METHOD_EC:  # Entity-centric TTI
            types = self.__entity_centric(query)
        else:  # default Type-centric TTI
            types = self.__type_centric(query)

        # sorts types
        sorted_types = {}
        i = 0
        for type_id, en in sorted(types.items(), key=lambda item: item[1]["score"], reverse=True):
            rank = i + self.__start
            sorted_types[rank] = {"type": type_id, "score": en["score"]}
            i += 1
            if i == self.__num_docs:
                break

        # converts to output format
        res = {"query": query,
               "results": sorted_types}

        return res

    def batch_identification(self):
        """Annotates, in a batch, queries with identified target types, and outputs results."""
        queries = json.load(open(expanduser(self.__query_file)))

        results = {}
        for query_id in sorted(queries):
            print("Identifying target types for [{}] {}".format(query_id, queries[query_id]))
            results[query_id] = self.identify(queries[query_id])
        json.dump(results, open(expanduser(self.__output_file), "w"), indent=4, sort_keys=True)
        print("Output file:", self.__output_file)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="query string", type=str, default=None)
    parser.add_argument("-c", "--config", help="config file", type=str, default={})
    args = parser.parse_args()

    return args


def main(args):
    config = FileUtils.load_config(args.config)
    tti = TTI(config)

    if args.query:
        res = tti.identify(args.query)
        pprint(res)
    else:
        tti.batch_identification()


if __name__ == '__main__':
    main(arg_parser())
