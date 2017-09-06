"""
Target Type Identification
==========================

The command-line application for target type indentification.

Usage
-----

::

  python -m nordlys.services.er <config_file> -q <query>

If `-q <query>` is passed, it returns the results for the specified query and prints them in terminal.

Config parameters
------------------

- **method**: name of TTI method; accepted values: ["tc", "ec", "ltr"]
- **num_docs**: number of documents to return
- **start**: starting offset for ranked documents
- **model**: retrieval model, if method is "tc" or "ec"; accepted values: ["lm", "bm25"]
- **ec_cutoff**: if method is "ec", rank cut-off of top-*K* entities for EC TTI
- **field**: field name, if method is "tc" or "ec"
- **smoothing_method**: accepted values: ["jm", "dirichlet"]
- **smoothing_param**: value of lambda or mu; accepted values: [float or "avg_len"]
- **query_file**: path to query file (JSON)
- **output_file**: path to output file (JSON)
- **trec_output_file**: path to output file (trec_eval-formatted)

Example config
---------------

.. code:: python

    { "method": "ec",
      "num_docs": 10,
      "model": "lm",
      "first_pass": {
          "num_docs": 50
      },
      "smoothing_method": "dirichlet",
      "smoothing_param": 2000,
      "ec_cutoff": 20,
	  "query_file": "path/to/queries.json",
	  "output_file": "path/to/output.txt",
	}
------------------------

:Author: Dario Garigliotti
"""

# -------

# Standard imports
from os.path import expanduser
import argparse
import json
from pprint import pprint

# Cross-ref imports
from nordlys.config import ELASTIC_INDICES, ELASTIC_TTI_INDICES
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.utils.file_utils import FileUtils
from nordlys.core.retrieval.retrieval import Retrieval  # for TC TTI
from nordlys.core.retrieval.scorer import Scorer  # for TC TTI
from nordlys.logic.fusion.late_fusion_scorer import LateFusionScorer  # for EC TTI
from nordlys.logic.entity.entity import Entity  # for defining the higher-order entity-centric late-fusion assoc func
from nordlys.core.utils.file_utils import FileUtils  # for outputting
from nordlys.core.retrieval.retrieval_results import RetrievalResults  # for TREC-formatted outputting
from nordlys.config import PLOGGER  # for logging

# -------

# DBpedia distinguished metadata
RDF_TYPE_PROP = "<rdf:type>"
OWL_THING_TYPE = "<owl:Thing>"
DBO_TYPE_PREFIX = "<dbo:"

# Methods and models
TTI_METHOD_TC = "tc"
TTI_METHOD_EC = "ec"
TTI_MODEL_BM25 = "bm25"
TTI_MODEL_LM = "lm"

# Default values for several parameters
DEFAULT_1ST_PASS_NUM_DOCS = 50  # Efficiency-related setting; it should be enough for types
DEFAULT_1ST_PASS_FIELD = "content"

DEFAULT_TTI_METHOD = TTI_METHOD_TC
DEFAULT_TTI_NUM_DOCS = 10  # enough for displaying top types
DEFAULT_TTI_START = 0
DEFAULT_TTI_TC_INDEX = ELASTIC_TTI_INDICES[0]
DEFAULT_TTI_EC_INDEX = ELASTIC_INDICES[0]
DEFAULT_TTI_EC_K_CUTOFF = 20  # Known to be a sufficient cut-off


# -------

class TTI(object):
    def __init__(self, config):
        self.__check_config(config)
        self.__config = config
        self.__method = config["method"]
        self.__num_docs = config["num_docs"]
        self.__start = config["start"]
        self.__tc_config = {  # only for TC TTI
            "index_name": self.__config["index"],
            "first_pass": {
                "1st_num_docs": DEFAULT_1ST_PASS_NUM_DOCS,
                "field": DEFAULT_1ST_PASS_FIELD
            },
        }
        self.__query_file = config.get("query_file", None)
        self.__output_file = config.get("output_file", None)

    @staticmethod
    def __check_config(config):
        """Checks config parameters and set default values."""
        config["method"] = config.get("method", TTI_METHOD_TC)  # TODO decide
        config["index"] = DEFAULT_TTI_TC_INDEX if config["method"] == TTI_METHOD_TC else DEFAULT_TTI_EC_INDEX
        config["num_docs"] = int(config.get("num_docs", DEFAULT_TTI_NUM_DOCS))
        config["start"] = int(config.get("start", DEFAULT_TTI_START))
        config["run_id"] = config.get("run_id", "tti")

        return config

    def __valid_final_ec_type(self, t):
        """Assesses whether a DBpedia type t is valid to be returned for the entity-centric mapper.

        :param t: a DBpedia type shortly-prefixed URI, e.g., "<dbo:City>".
        :type t: str
        :return: a Boolean value assessing whether t is valid.
        """
        return t is not OWL_THING_TYPE and t.startswith(DBO_TYPE_PREFIX)

    def __entity_centric_mapper(self, entity_id):
        """Gets the list of DBpedia types for a given entityID."""
        en = Entity()
        all_types = en.lookup_en(entity_id).get(RDF_TYPE_PROP, [])
        final_types = [t for t in all_types if self.__valid_final_ec_type(t)]  # filtering
        return final_types

    def __entity_centric(self, query):
        """Entity-centric TTI.

        :param query: query string
        :type query: str
        """
        types = dict()  # to be returned

        # Set the configurations
        model = self.__config.get("model", TTI_MODEL_BM25)
        ec_cutoff = self.__config.get("ec_cutoff", DEFAULT_TTI_EC_K_CUTOFF)
        self.__ec_retr_config = dict()
        for param in ["smoothing_method", "smoothing_param"]:
            if self.__config.get(param, None) is not None:
                self.__ec_retr_config[param] = self.__config.get(param)

        # Perform EC TTI using late fusion support
        late_fusion_scorer = LateFusionScorer(self.__config["index"], model, self.__ec_retr_config,
                                              num_docs=ec_cutoff, field="catchall", run_id=self.__config["run_id"],
                                              num_objs=self.__config["num_docs"])
        ret_res = late_fusion_scorer.score_query(query, assoc_fun=self.__entity_centric_mapper)

        for doc_id, score in ret_res.get_scores_sorted():
            types[doc_id] = {"score": score}
            PLOGGER.info("done")

        return types

    def __type_centric(self, query):
        """Type-centric TTI.

        :param query: query string
        :type query: str
        """
        types = dict()
        model = self.__config.get("model", TTI_MODEL_BM25)
        elastic = ElasticCache(self.__tc_config.get("index", DEFAULT_TTI_TC_INDEX))

        if model == TTI_MODEL_BM25:
            PLOGGER.info("TTI, TC, BM25")
            self.__tc_config["model"] = "bm25"
            # scorer = Scorer.get_scorer(elastic, query, self.__tc_config)
            types = Retrieval(self.__tc_config).retrieve(query)

        elif model == TTI_MODEL_LM:
            PLOGGER.debug("TTI, TC, LM")
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

            PLOGGER.info(types)

        return types

    def identify(self, query):
        """Performs target type identification for the query.

        :param query: query string
        :type query: str
        :return: annotated query
        """
        # obtains types according to requested method
        method = self.__config.get("method", None)
        if method == TTI_METHOD_EC:  # Entity-centric TTI
            types = self.__entity_centric(query)
        else:  # default Type-centric TTI
            types = self.__type_centric(query)

        # sorts types
        sorted_types = dict()
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
        queries = json.load(FileUtils.open_file_by_type(self.__query_file))

        f_trec_out = None
        if "trec_output_file" in self.__config:  # for TREC-formatted outputting
            f_trec_out = FileUtils.open_file_by_type(self.__config["trec_output_file"], mode="w")

        results = dict()
        for query_id in sorted(queries):
            PLOGGER.info("Identifying target types for [{}] {}".format(query_id, queries[query_id]))
            results[query_id] = self.identify(queries[query_id])

            # Output resulting scores in TREC format if required
            if f_trec_out:
                type_to_score = dict()
                for d in results.get(query_id, {}).get("results", {}).values():
                    type_to_score[d["type"]] = d["score"]
                ret_res = RetrievalResults(type_to_score)
                ret_res.write_trec_format(query_id,
                                          self.__config["run_id"],
                                          f_trec_out,
                                          max_rank=self.__config["num_docs"])

        json.dump(results, FileUtils.open_file_by_type(self.__output_file, mode="w"), indent=4, sort_keys=True)
        PLOGGER.info("Output file: {}".format(self.__output_file))

        if f_trec_out:
            f_trec_out.close()


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="query string", type=str, default=None)
    parser.add_argument("-c", "--config", help="config file", type=str, default=dict())
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
