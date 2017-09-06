"""
Scorer
======

Various retrieval models for scoring a individual document for a given query.

:Authors: Faegheh Hasibi, Krisztian Balog
"""
import math
import sys

from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.config import PLOGGER


class Scorer(object):
    """Base scorer class."""

    SCORER_DEBUG = 0

    def __init__(self, elastic, query, params):
        self._elastic = elastic
        self._query = query
        self._params = params

        # The analyser might return terms that are not in the collection.
        # These terms are filtered out later in the score_doc functions.
        if self._query:
            self._query_terms = elastic.analyze_query(self._query).split()
        else:
            self._query_terms = []

    # def score_doc(self, doc_id):
    #     """Scorer method to be implemented in each subclass."""
    #     # should use elastic scoring
    #     query = self._elastic.analyze_query(self._query)
    #     field = params["first_pass"]["field"]
    #     res = self._elastic.search(query, field, num=self.__first_pass_num_docs, start=start)
    #     return

    @staticmethod
    def get_scorer(elastic, query, config):
        """Returns Scorer object (Scorer factory).

        :param elastic: Elastic object
        :param query: raw query (to be analyzed)
        :param config: dict with models parameters
        """
        model = config.get("model", None)
        if model == "lm":
            PLOGGER.debug("\tLM scoring ... ")
            return ScorerLM(elastic, query, config)
        elif model == "mlm":
            PLOGGER.debug("\tMLM scoring ...")
            return ScorerMLM(elastic, query, config)
        elif model == "prms":
            PLOGGER.debug("\tPRMS scoring ...")
            return ScorerPRMS(elastic, query, config)
        elif model is None:
            return None
        else:
            raise Exception("Unknown model " + model)


# =========================================
# ================== LM  ==================
# =========================================
class ScorerLM(Scorer):
    """Language Model (LM) scorer."""
    JM = "jm"
    DIRICHLET = "dirichlet"

    def __init__(self, elastic, query, params):
        super(ScorerLM, self).__init__(elastic, query, params)
        self._field = params.get("fields", Elastic.FIELD_CATCHALL)
        self._smoothing_method = params.get("smoothing_method", self.DIRICHLET).lower()
        if self._smoothing_method == self.DIRICHLET:
            self._smoothing_param = params.get("smoothing_param", 2000)
        elif self._smoothing_method == ScorerLM.JM:
            self._smoothing_param = params.get("smoothing_param", 0.1)
        # self._smoothing_param = params.get("smoothing_param", None)
        else:
            PLOGGER.error(self._smoothing_method + " smoothing method is not supported!")
            sys.exit(0)

        self._tf = {}

    @staticmethod
    def get_jm_prob(tf_t_d, len_d, tf_t_C, len_C, lambd):
        """Computes JM-smoothed probability.
        p(t|theta_d) = [(1-lambda) tf(t, d)/|d|] + [lambda tf(t, C)/|C|]

        :param tf_t_d: tf(t,d)
        :param len_d: |d|
        :param tf_t_C: tf(t,C)
        :param len_C: |C| = \sum_{d \in C} |d|
        :param lambd: \lambda
        :return: JM-smoothed probability
        """
        p_t_d = tf_t_d / len_d if len_d > 0 else 0
        p_t_C = tf_t_C / len_C if len_C > 0 else 0
        if Scorer.SCORER_DEBUG:
            print("\t\t\tp(t|d) = {}\tp(t|C) = {}".format(p_t_d, p_t_C))
        return (1 - lambd) * p_t_d + lambd * p_t_C

    @staticmethod
    def get_dirichlet_prob(tf_t_d, len_d, tf_t_C, len_C, mu):
        """Computes Dirichlet-smoothed probability.
        P(t|theta_d) = [tf(t, d) + mu P(t|C)] / [|d| + mu]

        :param tf_t_d: tf(t,d)
        :param len_d: |d|
        :param tf_t_C: tf(t,C)
        :param len_C: |C| = \sum_{d \in C} |d|
        :param mu: \mu
        :return: Dirichlet-smoothed probability
        """
        if mu == 0:  # i.e. field does not have any content in the collection
            return 0
        else:
            p_t_C = tf_t_C / len_C if len_C > 0 else 0
            return (tf_t_d + mu * p_t_C) / (len_d + mu)

    def __get_term_freq(self, doc_id, field, term):
        """Returns the (cached) term frequency."""
        if doc_id not in self._tf:
            self._tf[doc_id] = {}
        if field not in self._tf[doc_id]:
            self._tf[doc_id][field] = self._elastic.term_freqs(doc_id, field)
        return self._tf[doc_id][field].get(term, 0)

    def get_lm_term_prob(self, doc_id, field, t, tf_t_d_f=None, tf_t_C_f=None):
        """Returns term probability for a document and field.

        :param doc_id: document ID
        :param field: field name
        :param t: term
        :return: P(t|d_f)
        """
        len_d_f = self._elastic.doc_length(doc_id, field)
        len_C_f = self._elastic.coll_length(field)
        tf_t_C_f = self._elastic.coll_term_freq(t, field) if tf_t_C_f is None else tf_t_C_f
        tf_t_d_f = self.__get_term_freq(doc_id, field, t) if tf_t_d_f is None else tf_t_d_f
        if self.SCORER_DEBUG:
            print("\t\tt = {}\t f = {}".format(t, field))
            print("\t\t\tDoc:  tf(t,f) = {}\t|f| = {}".format(tf_t_d_f, len_d_f))
            print("\t\t\tColl: tf(t,f) = {}\t|f| = ".format(tf_t_C_f, len_C_f))

        p_t_d_f = 0
        # JM smoothing: p(t|theta_d_f) = [(1-lambda) tf(t, d_f)/|d_f|] + [lambda tf(t, C_f)/|C_f|]
        if self._smoothing_method == self.JM:
            lambd = self._smoothing_param
            p_t_d_f = self.get_jm_prob(tf_t_d_f, len_d_f, tf_t_C_f, len_C_f, lambd)
            if self.SCORER_DEBUG:
                print("\t\t\tJM smoothing:")
                print("\t\t\tDoc:  p(t|theta_d_f)= ", p_t_d_f)

        # Dirichlet smoothing
        elif self._smoothing_method == self.DIRICHLET:
            mu = self._smoothing_param if self._smoothing_param != "avg_len" else self._elastic.avg_len(field)
            p_t_d_f = self.get_dirichlet_prob(tf_t_d_f, len_d_f, tf_t_C_f, len_C_f, mu)
            if self.SCORER_DEBUG:
                print("\t\t\tDirichlet smoothing:")
                print("\t\t\tmu: ", mu)
                print("\t\t\tDoc:  p(t|theta_d_f)= ", p_t_d_f)
        return p_t_d_f

    def get_lm_term_probs(self, doc_id, field):
        """Returns probability of all query terms for a document and field; i.e. p(t|theta_d)

        :param doc_id: document ID
        :param field: field name
        :return: dictionary of terms with their probabilities
        """
        p_t_theta_d_f = {}
        for t in set(self._query_terms):
            p_t_theta_d_f[t] = self.get_lm_term_prob(doc_id, field, t)
        return p_t_theta_d_f

    def score_doc(self, doc_id):
        """Scores the given document using LM.
        p(q|theta_d) = \sum log(p(t|theta_d))

        :param doc_id: document id
        :return: LM score
        """
        if self.SCORER_DEBUG:
            print("Scoring doc ID=" + doc_id)

        p_t_theta_d = self.get_lm_term_probs(doc_id, self._field)
        if sum(p_t_theta_d.values()) == 0:  # none of query terms are in the field collection
            if self.SCORER_DEBUG:
                print("\t\tP(q|{}) = None".format(self._field))
            return None

        # p(q|theta_d) = sum log(p(t|theta_d)); we return log-scale values
        p_q_theta_d = 0
        for t in self._query_terms:
            # Skips the term if it is not in the field collection
            if p_t_theta_d[t] == 0:
                continue
            if self.SCORER_DEBUG:
                print("\t\tP({}|{}) = {}".format(t, self._field, p_t_theta_d[t]))
            p_q_theta_d += math.log(p_t_theta_d[t])
        if self.SCORER_DEBUG:
            print("P(d|q) = {}".format(p_q_theta_d))
        return p_q_theta_d


# =========================================
# ================== MLM  =================
# =========================================
class ScorerMLM(ScorerLM):
    """Mixture of Language Model (MLM) scorer.

    Implemented based on:
        Ogilvie, Callan. Combining document representations for known-item search. SIGIR 2003.
    """

    def __init__(self, elastic, query, params):
        super(ScorerMLM, self).__init__(elastic, query, params)
        self._field_weights = params.get("fields", {})
        if "fields" not in params:
            raise Exception("Field weights are not defined for MLM scoring!")

    def get_mlm_term_prob(self, doc_id, t):
        """Returns MLM probability for the given term and field-weights.
        p(t|theta_d) = sum(mu_f * p(t|theta_d_f))

        :param lucene_doc_id: internal Lucene document ID
        :param t: term
        :return: P(t|theta_d)
        """
        p_t_theta_d = 0
        for f, mu_f in self._field_weights.items():
            p_t_theta_d_f = self.get_lm_term_prob(doc_id, f, t)
            p_t_theta_d += mu_f * p_t_theta_d_f
        if self.SCORER_DEBUG:
            print("\t\tP(t|theta_d)=" + str(p_t_theta_d))
        return p_t_theta_d

    def get_mlm_term_probs(self, doc_id):
        """ Returns probability of all query terms for a document; i.e. p(t|theta_d)

        :param doc_id: internal Lucene document ID
        :return: dictionary of terms with their probabilities
        """
        p_t_theta_d = {}
        for t in set(self._query_terms):
            p_t_theta_d[t] = self.get_mlm_term_prob(doc_id, t)
        return p_t_theta_d

    def score_doc(self, doc_id):
        """Scores the given document using MLM model.
        p(q|theta_d) = \sum log(p(t|theta_d))

        :param doc_id: document ID
        :return: MLM score of document and query
        """
        if self.SCORER_DEBUG:
            print("Scoring doc ID=" + doc_id)

        p_t_theta_d = self.get_mlm_term_probs(doc_id)
        if sum(p_t_theta_d.values()) == 0:  # none of query terms are in the field collection
            if self.SCORER_DEBUG:
                print("\t\tP_mlm(q|theta_d) = None")
            return None

        # p(q|theta_d) = sum(log(p(t|theta_d))) ; we return log-scale values
        p_q_theta_d = 0
        for t in self._query_terms:
            if p_t_theta_d[t] == 0:  # Skips the term if it is not in the field collection
                continue
            if self.SCORER_DEBUG:
                print("\tP_mlm({}|theta_d) = {}".format(t, p_t_theta_d[t]))
            p_q_theta_d += math.log(p_t_theta_d[t])
        if self.SCORER_DEBUG:
            print("P(d|q) = {}".format(p_q_theta_d))
        return p_q_theta_d


# =========================================
# ================= PRMS ==================
# =========================================
class ScorerPRMS(ScorerLM):
    """PRMS scorer."""

    # @todo: make this class similar to MLM scorer, add get_term_prob(s) functions

    def __init__(self, elastic, query, params):
        super(ScorerPRMS, self).__init__(elastic, query, params)
        self._fields = params["fields"]

        self.total_field_freq = None
        self.mapping_probs = None

    def score_doc(self, doc_id):
        """
        Scores the given document using PRMS model.

        :param doc_id: document id
        :param lucene_doc_id: internal Lucene document ID
        :return: float, PRMS score of document and query
        """
        if self.SCORER_DEBUG:
            print("Scoring doc ID=" + doc_id)

        # gets mapping probs: p(f|t)
        p_f_t = self.get_mapping_probs()

        # gets term probs: p(t|theta_d_f)
        p_t_theta_d_f = {}
        for field in self._fields:
            p_t_theta_d_f[field] = self.get_lm_term_probs(doc_id, field)
        # none of query terms are in the field collection
        if sum([sum(p_t_theta_d_f[field].values()) for field in p_t_theta_d_f]) == 0:
            return None

        # p(q|theta_d) = prod(p(t|theta_d)) ; we return log(p(q|theta_d))
        p_q_theta_d = 0
        for t in self._query_terms:
            if self.SCORER_DEBUG:
                print("\tt=" + t)
            # p(t|theta_d) = sum(p(f|t) * p(t|theta_d_f))
            p_t_theta_d = 0
            for f in self._fields:
                if f in p_f_t[t]:
                    p_t_theta_d += p_f_t[t][f] * p_t_theta_d_f[f][t]
                    if self.SCORER_DEBUG:
                        print("\t\t\tf = {}\tp(t|f) = {}\tP(t|theta_d,f) = {}".format(
                            f, p_f_t[t][f], p_t_theta_d_f[f][t]))

            if p_t_theta_d == 0:
                continue
            p_q_theta_d += math.log(p_t_theta_d)
            if self.SCORER_DEBUG:
                print("\t\tP(t|theta_d)= {}".format(p_t_theta_d))
        return p_q_theta_d

    def get_mapping_probs(self):
        """Gets (cached) mapping probabilities for all query terms."""
        if self.mapping_probs is None:
            self.mapping_probs = {}
            for t in set(self._query_terms):
                self.mapping_probs[t] = self.get_mapping_prob(t)
        return self.mapping_probs

    def get_mapping_prob(self, t, coll_termfreq_fields=None):
        """
        Computes PRMS field mapping probability.
            p(f|t) = P(t|f)P(f) / sum_f'(P(t|C_{f'_c})P(f'))

        :param t: str
        :param coll_termfreq_fields: {field: freq, ...}
        :return: a dictionary {field: prms_prob, ...}
        """
        if coll_termfreq_fields is None:
            coll_termfreq_fields = {}
            for f in self._fields:
                coll_termfreq_fields[f] = self._elastic.coll_term_freq(t, f)

        # calculates numerators for all fields: P(t|f)P(f)
        numerators = {}
        for f in self._fields:
            p_t_f = coll_termfreq_fields[f] / self._elastic.coll_length(f)
            p_f = self._elastic.doc_count(f) / self.get_total_field_freq()
            numerator = p_t_f * p_f
            if numerator > 0:
                numerators[f] = numerator
            if self.SCORER_DEBUG:
                print("\tf= {}\tt= {}\tP(t|f)= {}\tP(f)= {}".format(f, t, p_t_f, p_f))

        # calculates denominator: sum_f'(P(t|C_{f'_c})P(f'))
        denominator = sum(numerators.values())

        mapping_probs = {}
        if denominator > 0:  # if the term is present in the collection
            for f in numerators:
                mapping_probs[f] = numerators[f] / denominator
                if self.SCORER_DEBUG:
                    print("\t\tf= {}\tt= {}\tp(f|t)= {}/{} = {}".format(
                        f, t, numerators[f], sum(numerators.values()), mapping_probs[f]))

        return mapping_probs

    def get_total_field_freq(self):
        """Returns total occurrences of all fields"""
        if self.total_field_freq is None:
            total_field_freq = 0
            for f in self._fields:
                total_field_freq += self._elastic.doc_count(f)
            self.total_field_freq = total_field_freq
        return self.total_field_freq


if __name__ == "__main__":
    query = "gonna friends"
    doc_id = "4"
    es = ElasticCache("toy_index")
    params = {"fields": "content",
              "__fields": {"title": 0.2, "content": 0.8},
              "__fields": ["content", "title"]
              }
    score = ScorerPRMS(es, query, params).score_doc(doc_id)
    print(score)
