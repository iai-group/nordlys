"""
trec_eval
---------

Wrapper for trec_eval.

@author: Dario Garigliotti
@author: Shuo Zhang
"""

from subprocess import Popen, PIPE
from shlex import split

from nordlys.config import TREC_EVAL


class TrecEval(object):
    """Holds evaluation results obtained using trec_eval."""

    __TREC_EVAL_FLAGS = "-c -m all_trec -q"

    def __init__(self):
        self.__results = None  # results[query_id][metric] = score

    def __eval_proc(self, qrels_file, run_file, eval_file=None):
        """Executes the evaluation process call and optionally saves the output to a file.

        :param qrels_file: name of qrels file
        :param run_file: name of run file
        :param eval_file: name of evaluation output file
        """

        cmd_flags = " ".join([TREC_EVAL, self.__TREC_EVAL_FLAGS, qrels_file, run_file])

        if eval_file is not None:
            # TODO save output to file
            pass

        p = Popen(split(cmd_flags), stdout=PIPE)
        output, err = p.communicate()
        output = output.decode('utf8')
        return output, err

    def load_results(self, eval_file):
        """Loads results from an existing evaluation file.

        :param eval_file: name of evaluation file
        """
        self.__results = {}
        # TODO
        pass

    def evaluate(self, qrels_file, run_file, eval_file=None):
        """Evaluates a runfile using trec_eval. Optionally writes evaluation output to file.

        :param qrels_file: name of qrels file
        :param run_file: name of run file
        :param eval_file: name of evaluation output file
        """
        self.__results = {}
        output, _ = self.__eval_proc(qrels_file, run_file, eval_file=eval_file)

        for line in output.splitlines():
            metric, query_id, score = line.split()
            metric = metric.lower()

            if query_id == "all":  # ignore "all" lines
                continue

            try:
                score = float(score)
            except ValueError:  # e.g. some bad-formed lines with a "score" like '----------'
                continue

            query_data = self.__results.get(query_id, {})
            query_data[metric] = score
            self.__results[query_id] = query_data

    def get_query_ids(self):
        """Returns the set of queryIDs for which we have results."""
        return self.__results.keys()

    def get_score(self, query_id, metric):
        """Returns the score for a given queryID and metric.

        :param query_id: queryID
        :param metric: metric
        :return: score (or None if not found)
        """
        return self.__results.get(query_id, {}).get(metric.lower(), None)
