"""
eval
----

Console application for eval package.

@author: Faegheh Hasibi
"""

import argparse
from nordlys.core.eval.query_diff import QueryDiff

class Eval(object):
    """Main entry point for eval package.

    :param operation: operation (see :py:const:`OPERATIONS` for allowed values)
    :param qrels: name of qrels file
    :param runs: name of run files
    :param metric: metric
    """

    OP_QUERY_DIFF = "query_diff"
    OPERATIONS = [OP_QUERY_DIFF]

    def __init__(self, operation, qrels=None, runs=None, metric=None, output_file=None):
        self.__operation = operation
        self.__qrels = qrels
        self.__runs = runs
        self.__metric = metric
        self.__output_file = output_file

    def run(self):
        """Runs the operation with the given arguments."""
        if self.__operation == self.OP_QUERY_DIFF:
            qd = QueryDiff(self.__runs[0], self.__runs[1], self.__qrels, self.__metric)
            qd.dump_differences(self.__output_file)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", help="operation", type=str, choices=Eval.OPERATIONS, required=True)
    parser.add_argument("-q", "--qrels", help="qrels file", type=str)
    parser.add_argument("-r", "--runs", help="run files, separated with space", nargs="+")
    parser.add_argument("-m", "--metric", help="evaluation metric (from trec_eval)", type=str)
    parser.add_argument("-f", "--output_file", help="output file", type=str)
    args = parser.parse_args()
    return args


def main(args):
    eval = Eval(args.operation, qrels=args.qrels, runs=args.runs, metric=args.metric, output_file=args.output_file)
    eval.run()


if __name__ == "__main__":
    main(arg_parser())
