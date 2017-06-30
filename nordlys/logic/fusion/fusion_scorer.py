"""
Fusion Scorer
=============

Abstract class for fusion-based scoring.

:Authors: Shuo Zhang, Krisztian Balog, Dario Garigliotti
"""

from nordlys.core.retrieval.retrieval import Retrieval

class FusionScorer(object):
    ASSOC_MODE_BINARY = 1
    ASSOC_MODE_UNIFORM = 2

    """Abstract class for any fusion-based method."""

    def __init__(self, index_name, association_file=None, run_id="fusion"):
        """
        :param index_name: name of index
        :param association_file: association file
        """
        self._index_name = index_name
        self.association_file = association_file
        self.assoc_obj = dict()
        self.assoc_doc = dict()
        self.run_id = run_id

    def load_associations(self):
        """Loads the document-object associations."""
        # file format: documentId objectId per line
        if self.association_file is not None:
            # you can keep the def here
            pass
        pass

    def score_query(self, query, assoc_fun=None):
        pass

    def score_queries(self, queries, output_file):
        """Scores all queries and optionally dumps results into an output file."""
        out = open(output_file, "w")
        for query_id in sorted(queries):
            query = queries[query_id]
            pqo = self.score_query(query)
            pqo.write_trec_format(query_id, self.run_id, out)
        out.close()

    def load_queries(self, query_file):
        """Loads the query file
        :return: query dictionary {queryID:query([term1,term2,...])}
        """
        f = open(query_file, "r")
        queries = {}
        for line in f:
            tmp = line.split()
            query_id = tmp[0]
            query = tmp[1:]
            queries[query_id] = query
        f.close()
        return queries

    # def parse(self, text):
    #     stopwords = [
    #         "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in",
    #         "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the",
    #         "their", "then", "there", "these", "they", "this", "to", "was", "will", "with"]
    #     terms = []
    #     # Replace specific characters with space
    #     chars = ["'", ".", ":", ",", "/", "(", ")", "-", "+"]
    #     for ch in chars:
    #         if ch in text:
    #             text = text.replace(ch, " ")
    #     # Tokenization
    #     for term in text.split():  # default behavior of the split is to split on one or more whitespaces
    #         # Lowercasing
    #         term = term.lower()
    #         # Stopword removal
    #         if term in stopwords:
    #             continue
    #         terms.append(term)
    #     return terms
