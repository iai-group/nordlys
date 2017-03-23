"""Entity retrieval.

entity_retrieval
----------------

@author: Faegheh Hasibi
@author: Krisztian Balog
"""
import argparse
from pprint import pprint

from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.retrieval.retrieval import Retrieval
from nordlys.core.retrieval.scorer import Scorer
from nordlys.core.utils.file_utils import FileUtils


class ER(object):
    """Performs entity retrieval based on the given configuration.

    :param config: retrieval config (JSON config file or a dictionary) of the shape:

    ::

        {
            "index_name": name of the index,
            "first_pass": {
                "num_docs": number of documents in first-pass scoring (default: 100)
                "field": field used in first pass retrieval (default: Elastic.FIELD_CATCHALL)
                "fields_return": comma-separated list of fields to return for each hit (default: "")
            },
            "num_docs": number of documents to return (default: 100)
            "start": starting offset for ranked documents (default:0)
            "model": name of retrieval model; accepted values: [lm, mlm, prms] (default: lm)
            "field": field name for LM (default: catchall)
            "fields": list of fields for PRMS (default: [catchall])
            "field_weights": dictionary with fields and corresponding weights for MLM (default: {catchall: 1})
            "smoothing_method": accepted values: [jm, dirichlet] (default: dirichlet)
            "smoothing_param": value of lambda or mu; accepted values: [float or "avg_len"],
                                (jm default: 0.1, dirichlet default: 2000)

            "query_file": name of query file (JSON),
            "output_file": name of output file,
            "run_id": run id for TREC output
        }
    """

    def __init__(self, config):
        self.__check_config(config)
        self.__config = config
        self.__num_docs = int(config["num_docs"])
        self.__start = int(config["start"])
        self.__er = Retrieval(config)

    @staticmethod
    def __check_config(config):
        """Checks config parameters and set default values."""
        if config.get("first_pass", {}).get("num_docs", None) is None:
            config["first_pass"]["num_docs"] = 1000
        if config.get("num_docs", None) is None:
            config["num_docs"] = config["first_pass"]["num_docs"]
        if config.get("start", None) is None:
            config["start"] = 0
        # Todo: Check the ELR params
        return config

    def __get_scorer(self, query):
        """Factory method to get entity retrieval method."""
        model = self.__config.get("model", None)
        # if model == "elr":
        #     scorer = ELR(self.__config)
        # else:  # from core.retrieval
        elastic = ElasticCache(self.__config["index_name"])
        scorer = Scorer.get_scorer(elastic, query, self.__config)
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
        for i in range(self.__start, self.__start + self.__num_docs):
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
    er = ER(config)

    if args.query:
        res = er.retrieve(args.query)
        pprint(res)
    else:
        er.batch_retrieval()

if __name__ == '__main__':
    main(arg_parser())