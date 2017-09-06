"""
Query
=====

Class for representing a query.

TODO: add preprocessing using

:Author: Faegheh Hasibi
"""

import re


class Query(object):

    def __init__(self, query, qid=""):
        self.__qid = qid
        self.__raw_query = query
        self.__query = None  # holds preprocessed query
        self.__preprocess()  # always preprocess the query

    @property
    def query(self):
        return self.__query

    @property
    def raw_query(self):
        return self.__raw_query

    @property
    def qid(self):
        return self.__qid

    def __preprocess(self):
        """Pre-process the query; removes some special chars."""
        # TODO make preprocessing (including stopwords removal) using Retrieval package
        input_str = re.sub("[^A-Za-z0-9+-]+", " ", self.raw_query)
        input_str = input_str.replace(" OR ", " ").replace(" AND ", " ")
        # removing multiple spaces
        self.__query = ' '.join(input_str.split()).lower()

    def get_terms(self):
        """Gets query terms.

        :return: list of query terms
        """
        return self.query.split()

    def get_ngrams(self):
        """Finds all n-grams of the query.

        :return: list of n-grams
        """
        terms = self.get_terms()
        ngrams = []
        for i in range(1, len(terms) + 1):  # number of words
            for start in range(0, len(terms) - i + 1):  # start point
                ngram = terms[start]
                for j in range(1, i):  # builds the sub-string
                    ngram += " " + terms[start + j]
                ngrams.append(ngram)
        return ngrams