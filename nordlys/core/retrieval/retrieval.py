"""
retrieval
---------

Console application for general-purpose retrieval.

* *First pass*: get top ``N`` documents using Elastic's default retrieval method (based on the catch-all content field)
* *Second pass*: perform (expensive) scoring of the top ``N`` documents using the Scorer class

@author: Krisztian Balog
@author: Faegheh Hasibi
"""
import argparse
import json
import sys

from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.retrieval.scorer import Scorer, ScorerLM
from nordlys.core.utils.file_utils import FileUtils


class Retrieval(object):
    """Loads config file, checks params, and sets default values.

    :param config: retrieval config (JSON config file or a dictionary) of the shape:
    ::
        {
            "index_name": name of the index,
            "first_pass": {
                "num_docs": number of documents in first-pass scoring (default: 1000)
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
    FIELDED_MODELS = {"mlm", "prms"}
    LM_MODELS = {"lm", "mlm", "prms"}

    def __init__(self, config):
        self.check_config(config)
        self.__config = config
        self.__index_name = config["index_name"]
        self.__first_pass_num_docs = int(config["first_pass"]["num_docs"])
        self.__first_pass_field = config["first_pass"]["field"]
        self.__first_pass_fields_return = config["first_pass"]["fields_return"]
        self.__first_pass_model = config["first_pass"]["model"]
        self.__start = int(config["start"])
        self.__model = config.get("model", None)
        self.__num_docs = int(config.get("num_docs", None))
        self.__query_file = config.get("query_file", None)
        self.__output_file = config.get("output_file", None)
        self.__run_id = config.get("run_id", self.__model)

        self.__elastic = ElasticCache(self.__index_name)

    @staticmethod
    def check_config(config):
        """Checks config parameters and sets default values."""
        try:
            if config.get("index_name", None) is None:
                raise Exception("index_name is missing")

            # Checks first pass parameters
            if config.get("first_pass", None) is None:
                config["first_pass"] = {}
            if config["first_pass"].get("num_docs", None) is None:
                config["first_pass"]["num_docs"] = 1000
            if config["first_pass"].get("field", None) is None:
                config["first_pass"]["field"] = Elastic.FIELD_CATCHALL
            if config["first_pass"].get("fields_return", None) is None:
                config["first_pass"]["fields_return"] = ""
            if config["first_pass"].get("model", None) is None:
                config["first_pass"]["model"] = Elastic.BM25

            if config.get("start", None) is None:
                config["start"] = 0
            if config.get("num_docs", None) is None:
                config["num_docs"] = 100

            if config.get("model", None) is None:
                config["model"] = None
            if config.get("field", None) is None:
                config["field"] = Elastic.FIELD_CATCHALL
            if config.get("fields", None) is None:
                config["fields"] = [Elastic.FIELD_CATCHALL]
            if config.get("field_weights", None) is None:
                config["field_weights"] = {Elastic.FIELD_CATCHALL: 1}
            if config["model"] in Retrieval.LM_MODELS:
                if config.get("smoothing_method", None) is None:
                    config["smoothing_method"] = ScorerLM.DIRICHLET
                if config.get("smoothing_param", None) is None:
                    if config["smoothing_method"] == ScorerLM.DIRICHLET:
                        config["smoothing_param"] = 2000
                    elif config["smoothing_method"] == ScorerLM.JM:
                        config["smoothing_param"] = 0.1
                    else:
                        raise Exception("Smoothing method is not supported.")
        except Exception as e:
            print("Error in config file: ", e)
            sys.exit(1)

    def _first_pass_scoring(self, analyzed_query):
        """Returns first-pass scoring of documents.

        :param analyzed_query: analyzed query
        :return: RetrievalResults object
        """
        print("\tFirst pass scoring... ", )
        # todo: add support for other similarities
        # body = {"query": {
        #     "bool": {
        #         "should": [
        #             {"match": {
        #                 "catchall": {
        #                     "query": analyzed_query
        #                 }}},
        #             {"match": {
        #                 "names": {
        #                     "query": analyzed_query,
        #                     "boost": 3
        #                 }}}]}}}
        # self.__elastic.update_similarity(self.__first_pass_model, self.__first_pass_model_params)
        res1 = self.__elastic.search(analyzed_query, self.__first_pass_field, num=self.__first_pass_num_docs,
                                     fields_return=self.__first_pass_fields_return)
        # res1 = self.__elastic.search_complex(body=body, num=self.__first_pass_num_docs,
        #                              fields_return=self.__first_pass_fields_return)
        return res1

    def _second_pass_scoring(self, res1, scorer):
        """Returns second-pass scoring of documents.

        :param res1: first pass results
        :param scorer: scorer object
        :return: RetrievalResults object
        """
        print("\tSecond pass scoring... ", )
        res2 = {}
        for doc_id in res1.keys():
            res2[doc_id] = {"score": scorer.score_doc(doc_id), "fields": res1[doc_id].get("fields", {})}
        print("done")
        return res2

    def retrieve(self, query, scorer=None):
        """Scores documents for the given query."""
        query = self.__elastic.analyze_query(query)

        # 1st pass retrieval
        res1 = self._first_pass_scoring(query)
        if self.__model is None:
            return res1

        # 2nd pass retrieval
        scorer = scorer if scorer else Scorer.get_scorer(self.__elastic, query, self.__config)
        res2 = self._second_pass_scoring(res1, scorer)
        return res2

    def batch_retrieval(self):
        """Scores queries in a batch and outputs results."""
        queries = json.load(open(self.__query_file))

        # init output file
        open(self.__output_file, "w").write("")
        out = open(self.__output_file, "w")

        # retrieves documents
        for query_id in sorted(queries):
            print("scoring [" + query_id + "] " + queries[query_id])
            results = self.retrieve(queries[query_id])
            out.write(self.trec_format(results, query_id, self.__num_docs))
        out.close()
        print("Output file:", self.__output_file)

    def trec_format(self, results, query_id, max_rank=100):
        """Outputs results in TREC format"""
        out_str = ""
        rank = 1
        for doc_id, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
            if rank > max_rank:
                break
            out_str += query_id + "\tQ0\t" + doc_id + "\t" + str(rank) + "\t" + str(score) + "\t" + self.__run_id + "\n"
            rank += 1
        return out_str


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


def main(args):
    example_config = {"index_name": "toy_index",
                      # "query_file": "data/queries/test_queries.json",
                      "first_pass": {
                          "num_docs": 1000,
                          "field": "content",
                          # "model": "LMJelinekMercer",
                          # "model_params": {"lambda": 0.1}
                      },
                      "second_pass": {
                          "field": "content",
                          "model": "lm",
                          "smoothing_method": "jm",
                          "smoothing_param": 0.1
                      },
                      "output_file": "output/test_retrieval.txt"
                      }
    config = FileUtils.load_config(args.config) if args.config != "" else example_config
    r = Retrieval(config)
    r.batch_retrieval()


if __name__ == "__main__":
    main(arg_parser())
