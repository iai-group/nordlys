"""
Retrieval Results
=================

Result list representation.

  - for each hit it holds score and both internal and external doc_ids

:Authors: Faegheh Hasibi, Krisztian Balog
"""

import operator


class RetrievalResults(object):
    """Class for storing retrieval scores for a given query."""
    def __init__(self, scores={}, query=None):
        self.__scores = scores
        self.__query = query

    @classmethod
    def elastic_to_retrieval(cls, res, query=None):
        """Converts elastic search results to retrieval results."""
        scores = dict()
        for hit in res['hits']:
            scores[hit['_id']] = hit["_score"]
        results = cls(scores=scores, query=query)
        return results

    @property
    def query(self):
        return self.__query

    def append(self, doc_id, score):
        """Adds document to the result list"""
        self.__scores[doc_id] = score

    def num_docs(self):
        """Returns the number of documents in the result list."""
        return len(self.__scores)

    def get_score(self, doc_id):
        """Returns the score of a document (or None if it's not in the list)."""
        return self.__scores.get(doc_id, None)

    def get_scores_sorted(self):
        """Returns all results sorted by score"""
        return sorted(self.__scores.items(), key=operator.itemgetter(1), reverse=True)

    def write_trec_format(self, query_id, run_id, out, max_rank=100):
        """Outputs results in TREC format"""
        rank = 1
        for doc_id, score in self.get_scores_sorted():
            if rank <= max_rank:
                out.write(query_id + "\tQ0\t" + doc_id + "\t" + str(rank) + "\t" + str(score) + "\t" + run_id + "\n")
            rank += 1