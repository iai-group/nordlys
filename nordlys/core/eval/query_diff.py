"""
Query Differences
=================

Computes query-level differences between two runs.

:Authors: Shuo Zhang, Krisztian Balog, Dario Garigliotti
"""

from nordlys.core.eval.trec_eval import TrecEval
from nordlys.core.utils.file_utils import FileUtils


class QueryDiff(object):
    def __init__(self, run1_file, run2_file, qrels, metric):
        """
        :param run1_file: name of run1 file (baseline)
        :param run2_file: name of run2 file (new method)
        :param qrels: name of qrels file
        :param metric: metric
        :return:
        """
        self.__run1_file = run1_file
        self.__run2_file = run2_file
        self.__qrels = qrels
        self.__metric = metric

    def dump_differences(self, output_file):
        """Outputs query-level differences between two methods into a tab-separated file.

        The first method is considered the baseline, the differences are with respect to that.
        Output format: queryID res1 res2 diff(res2-res1)
        """
        te_method1 = TrecEval()
        te_method1.evaluate(self.__qrels, self.__run1_file)
        te_method2 = TrecEval()
        te_method2.evaluate(self.__qrels, self.__run2_file)
        data = []
        for query_id in te_method1.get_query_ids():
            res1 = te_method1.get_score(query_id, self.__metric)
            res2 = te_method2.get_score(query_id, self.__metric)
            data.append([query_id, res1, res2, round(res2 - res1, 4)])

        # sorts based on the differences desc
        sorted_data = sorted(data, key=lambda l: l[3], reverse=True)

        FileUtils.dump_tsv(output_file, sorted_data, header=["queryID", "method1", "method2", "diff"])
