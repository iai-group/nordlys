"""
Trec Qrels
==========

Utility module for working with TREC qrels files.

Usage
-----

Get statistics about a qrels file
  ``trec_qrels <qrels_file> -o stat``


Filter qrels to contain only documents from a given set
  ``trec_qrels <qrels_file> -o filter_docs -d <doc_ids_file> -f <output_file>``


Filter qrels to contain only queries from a given set
  ``trec_qrels <qrels_file> -o filter_qs -q <query_ids_file> -f <output_file>``


:Author: Krisztian Balog
"""

import argparse
from nordlys.config import PLOGGER


class TrecQrels(object):
    """Represents relevance judments (TREC qrels)."""

    def __init__(self, file_name=None):
        self.__qrels = {}
        if file_name is not None:
            self.load(file_name)

    def load(self, file_name):
        """Loads qrels from file.

        :param file_name: name of qrels file
        """
        with open(file_name, "r") as f_qrels:
            for line in f_qrels:  # <query_id> <Q0> <doc_id> <relevance>
                result = line.strip().split()
                if len(result) == 4:
                    query_id, doc_id, rel = result[0], result[2], result[3]
                    if query_id not in self.__qrels:
                        self.__qrels[query_id] = {}
                    self.__qrels[query_id][doc_id] = rel

    def get_queries(self):
        """Returns the set of queries."""
        return self.__qrels.keys()

    def get_rel(self, query_id):
        """Returns relevance level for a given query.

        :param query_id: queryID
        :return: dict (docID as key and relevance as value) or None
        """
        return self.__qrels.get(query_id)

    def num_rel(self, query_id, min_rel=1):
        """Returns the number of relevant results for a given query.

        :param query_id: queryID
        :param min_rel: minimum relevance level
        :return: number of relevant results
        """
        if query_id not in self.__qrels:
            return None
        return sum(rel >= min_rel for rel in self.__qrels[query_id].values())

    def print_stat(self):
        """Prints simple statistics."""
        print("#queries:  " + str(len(self.__qrels)))
        print("#judments: " + str(sum(len(v) for k, v in self.__qrels.items())))

    def filter_by_doc_ids(self, doc_ids_file, output_file):
        """Filters qrels for a set of selected docIDs and outputs the results to a file.

        :param doc_ids_file: File with one docID per line
        :param output_file: Output file name
        """
        # loading docIDs (with ignoring empty lines in the input file)
        with open(doc_ids_file, "r") as f:
            doc_ids = [l for l in (line.strip() for line in f) if l]

        # filtering qrels
        with open(output_file, "w") as f:
            for query_id, res in self.__qrels.items():
                for doc_id, rel in res.items():
                    if doc_id in doc_ids:
                        f.write(query_id + " Q0 " + doc_id + " " + str(rel) + "\n")

    def filter_by_query_ids(self, query_ids_file, output_file):
        """Filters qrels for a set of selected queryIDs and outputs the results to a file.

        :param query_ids_file: File with one queryID per line
        :param output_file: Output file name
        """
        # loading docIDs (with ignoring empty lines in the input file)
        with open(query_ids_file, "r") as f:
            query_ids = [l for l in (line.strip() for line in f) if l]

        # filtering qrels
        with open(output_file, "w") as f:
            for query_id, res in self.__qrels.items():
                if query_id in query_ids:
                    for doc_id, rel in res.items():
                        f.write(query_id + " Q0 " + doc_id + " " + str(rel) + "\n")


CHOICE_STAT = "stat"
CHOICE_FILTER_DOCS = "filter_docs"
CHOICE_FILTER_QS = "filter_qs"


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("qrels_file", help="qrels file")  # mandatory arg
    parser.add_argument("-o", "--operation", help="operation name",
                        choices=[CHOICE_STAT, CHOICE_FILTER_DOCS, CHOICE_FILTER_QS])
    parser.add_argument("-d", "--doc_ids_file", help="file with the allowed doc_ids (for filtering)", type=str)
    parser.add_argument("-q", "--query_ids_file", help="file with the allowed query_ids (for filtering)",
                        type=str)
    parser.add_argument("-f", "--output_file", help="output file", type=str)
    args = parser.parse_args()
    return args


def main(args):
    qrels = TrecQrels(args.qrels_file)

    if args.operation == CHOICE_STAT:
        qrels.print_stat()
    elif args.operation == CHOICE_FILTER_DOCS:
        if len(args.doc_ids_file) == 0 or len(args.output_file) == 0:
            PLOGGER.info("doc_ids_file or output_file missing")
        else:
            qrels.filter_by_doc_ids(args.doc_ids_file, args.output_file)
    elif args.operation == CHOICE_FILTER_QS:
        if len(args.query_ids_file) == 0 or len(args.output_file) == 0:
            PLOGGER.info("query_ids_file or output_file missing")
        else:
            qrels.filter_by_query_ids(args.query_ids_file, args.output_file)


if __name__ == "__main__":
    main(arg_parser())
