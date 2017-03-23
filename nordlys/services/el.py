"""Entity linking.

entity_linking
--------------

@author: Faegheh Hasibi
"""

import argparse
import json
from pprint import pprint

from nordlys.core.utils.file_utils import FileUtils
from nordlys.logic.el.cmns import Cmns
from nordlys.logic.entity.entity import Entity
from nordlys.logic.query.query import Query


class EL(object):
    """Performs entity linking based on the given configuration.

        :param config: entity linking config (JSON config file or a dictionary) of the shape:

        ::

            {
                "method": name of the method,
                "threshold": entity linking threshold (varies depending on the method)
                "query_file": name of query file (JSON),
                "output_file": name of output file,
            }

    """
    def __init__(self, config, entity):
        self.__check_config(config)
        self.__config = config
        self.__method = config["method"]
        self.__threshold = float(config["threshold"])
        self.__query_file = config.get("query_file", None)
        self.__output_file = config.get("output_file", None)
        self.__entity = entity

    @staticmethod
    def __check_config(config):
        """Checks config parameters and set default values."""
        if config.get("method", None) is None:
            config["method"] = "cmns"
        if config.get("threshold", None) is None:
            if config["method"] == "cmns":
                config["threshold"] = 0.1
        return config

    def __get_linker(self, query):
        """Returns the entity linker based on the given model and parameters

        :param query: query object
        :return: entity linking object
        """
        if self.__method.lower() == "cmns":
            return Cmns(query, self.__entity, self.__threshold)
        else:
            raise Exception("Unknown model " + self.__method)

    def link(self, query):
        """Performs entity linking for the query.

        :param query: query string
        :return: annotated query
        """
        q = Query(query)
        linker = self.__get_linker(q)
        linked_ens = linker.link()
        res = {"query": q.raw_query,
               "processed_query": q.query,
               "results": linked_ens}
        return res

    def batch_linking(self):
        """Scores queries in a batch and outputs results."""
        queries = json.load(open(self.__query_file))

        results = {}
        for query_id in sorted(queries):
            print("linking [" + query_id + "] " + queries[query_id])
            results[query_id] = self.link(queries[query_id])
        json.dump(results, open(self.__output_file, "w"), indent=4, sort_keys=True)
        print("Output file:", self.__output_file)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="query string", type=str, default=None)
    parser.add_argument("-c", "--config", help="config file", type=str, default={})
    args = parser.parse_args()
    return args


def main(args):
    config = FileUtils.load_config(args.config)
    el = EL(config, Entity())

    if args.query:
        res = el.link(args.query)
        pprint(res)
    else:
        el.batch_linking()

if __name__ == '__main__':
    main(arg_parser())
