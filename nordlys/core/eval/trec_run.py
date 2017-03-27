"""
trec_run
--------

Utility module for working with TREC runfiles.

Usage:

Get statistics about a runfile
  ``trec_run <run_file> -o stat``


Filter runfile to contain only documents from a given set
  ``trec_run <run_file> -o filter -d <doc_ids_file> -f <output_file> -n <num_results>``


@author: Krisztian Balog
@author: Dario Garigliotti
"""

import argparse
from math import exp
from nordlys.core.retrieval.retrieval_results import RetrievalResults
from nordlys.core.storage.parser.uri_prefix import URIPrefix


class TrecRun(object):
    """Represents a TREC runfile.

    :param file_name: name of the run file
    :param normalize: whether retrieval scores are to be normalized for each query (default: False)
    :param remap_by_exp: whether scores are to be converted from the log-domain by taking their exp (default: False)
    """

    def __init__(self, file_name=None, normalize=False, remap_by_exp=False, run_id=None):
        self.__results = {}  # key is a query_id, value is a RetrievalResults object
        self.__sum_scores = {}
        self.run_id = run_id
        if file_name is not None:
            self.load_file(file_name, remap_by_exp)
            if normalize is True:
                self.normalize()

    def load_file(self, file_name, remap_by_exp=False):
        """Loads a TREC runfile.

        :param file_name: name of the run file
        :param remap_by_exp: whether scores are to be converted from the log-domain by taking their exp (default: False)
        """
        # load the file such that self.results[query_id] = res holds the results for a given query,
        # where res is a RetrievalResults object
        pre = URIPrefix()
        with open(file_name, "r") as f_baseline:
            for line in f_baseline:
                # Parse data
                fields = line.rstrip().split()
                if len(fields) != 6:
                    continue
                query_id, doc_id, score = fields[0], fields[2], float(fields[4])
                if self.run_id is None:
                    self.run_id = fields[5]

                # Add parsed data
                if query_id not in self.__results:
                    self.__results[query_id] = RetrievalResults()  # initialize
                # remap exponentially the scores in log-domain to (0, 1)
                if remap_by_exp:
                    score = exp(score)
                self.__results[query_id].append(doc_id, score)
                # an additional data structure to make the normalization easier
                self.__sum_scores[query_id] = self.__sum_scores.get(query_id, 0) + score

    def normalize(self):
        """Normalizes the retrieval scores such that they sum up to one for each query."""
        query_ids = self.get_results().keys()  # new var, since for-loop will modify this dict
        for query_id in query_ids:
            norm_result = RetrievalResults()
            for entity_id, score in self.get_results()[query_id].get_scores_sorted():
                norm_result.append(entity_id, score / self.__get_sum_scores(query_id))
            self.get_results()[query_id] = norm_result  # overwrite previous result

    def filter(self, doc_ids_file, output_file, num_results=100):
        """Filters runfile to include only selected docIDs and outputs the results to a file.

        :param doc_ids_file: file with one doc_id per line
        :param output_file: output file name
        :param num_results: number of results per query
        """
        # loading docids (with ignoring empty lines in the input file)
        with open(doc_ids_file, "r") as f:
            doc_ids = [l for l in (line.strip() for line in f) if l]

        # filtering qrels
        with open(output_file, "w") as f:
            for query_id, res in self.__results.items():
                filtered_res = RetrievalResults()
                for doc_id, score in res.get_scores_sorted():
                    if doc_id in doc_ids:
                        filtered_res.append(doc_id, score)
                    if filtered_res.num_docs() == num_results:
                        break
                filtered_res.write_trec_format(query_id, self.run_id, f, num_results)

    def get_query_results(self, query_id):
        """Returns the corresponding RetrievalResults object for a given query.

        :param query_id: queryID
        :rtype: :py:class:`nordlys.core.retrieval.retrieval_results.RetrievalResults`
        """
        return self.__results.get(query_id, None)

    def get_results(self):
        """Returns all results.

        :return: a dict with queryIDs as keys and RetrievalResults object as values
        """
        return self.__results

    def __get_sum_scores(self, query_id):
        """Returns the sum of all the retrieval scores for a given query.

        :param query_id: queryID
        :return: sum of scores (or None if the queryID cannot be found)
        """
        return self.__sum_scores.get(query_id, None)

    def print_stat(self):
        """Prints simple statistics."""
        print("#queries:  " + str(len(self.__results)))
        print("#results: " + str(sum(v.num_docs() for k, v in self.__results.items())))


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_file", help="run file")  # mandatory arg
    parser.add_argument("-o", "--operation", help="operation name", choices=["stat", "filter"])
    parser.add_argument("-d", "--doc_ids_file", help="file with the allowed doc_ids (for filtering)", type=str)
    parser.add_argument("-f", "--output_file", help="output file", type=str)
    parser.add_argument("-n", "--num_results", help="number of results", type=int)
    args = parser.parse_args()
    return args


def main(args):
    run = TrecRun(args.run_file)

    if args.operation == "stat":
        run.print_stat()
    elif args.operation == "filter":
        if len(args.doc_ids_file) == 0 or len(args.output_file) == 0:
            print("doc_ids_file or output_file missing")
        else:
            run.filter(args.doc_ids_file, args.output_file)


if __name__ == "__main__":
    main(arg_parser())