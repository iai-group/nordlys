"""
FTR Entity Similarity
=====================

Implements features capturing the similarity between entity and a query.

:Author: Faegheh Hasibi
"""

from __future__ import division
import re
import math

from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.scorer import ScorerMLM


class FtrEntitySimilarity(object):
    DEBUG = 0

    def __init__(self, query, en_id, elastic):
        self.__query = query
        self.__en_id = en_id
        self.__elastic = elastic

    def lm_score(self, field=Elastic.FIELD_CATCHALL):
        """
        Query length normalized LM score between entity field and query

        :param field: field name
        :return MLM score
        """
        raw_score = self.nllr(self.__query, {field: 1})
        score = math.exp(raw_score) if raw_score else 0
        return score

    def mlm_score(self, field_weights):
        """
        Query length normalized MLM similarity between the entity and query

        :param field_weights: dictionary {field: weight, ...}
        :return MLM score
        """
        raw_score = self.nllr(self.__query, field_weights)
        score = math.exp(raw_score) if raw_score else 0
        return score

    def context_sim(self, mention, field=Elastic.FIELD_CATCHALL):
        """
        LM score of entity to the context of query (context means query - mention)
            E.g. given the query "uss yorktown charleston" and mention "uss",
                query context is " yorktown charleston"

        :param mention: string
        :param field: field name
        :return context similarity score
        """
        # get query context
        match = re.search(mention, self.__query)
        if match is None:
            raise Exception("NOTE: Mention \"" + mention + "\" is not found in the query \"" + self.__query + "\"")
        mention_scope = match.span()
        q_context = self.__query[:mention_scope[0]] + self.__query[mention_scope[1]:]
        # scoring
        raw_score = self.nllr(q_context.strip(), {field: 1})
        score = math.exp(raw_score) if raw_score else 0
        return score

    def nllr(self, query, field_weights):
        """
        Computes Normalized query likelihood (NLLR):
            NLLR(q,d) = \sum_{t \in q} P(t|q) log P(t|\theta_d) - \sum_{t \in q} p(t|q) log P(t|C)
            where:
                P(t|q) = n(t,q)/|q|
                P(t|C) =  \sum_{f} \mu_f * P(t|C_f)
                P(t|\theta_d) = smoothed LM/MLM score

        :param query: query
        :param field_weights: dictionary {field: weight, ...}
        :return: NLLR score
        """
        query = self.__elastic.analyze_query(query)
        scorer_mlm = ScorerMLM(self.__elastic, query, {"fields": field_weights})
        term_probs = scorer_mlm.get_mlm_term_probs(self.__en_id)

        # none of query terms are in the collection
        if sum(term_probs.values()) == 0:
            if self.DEBUG:
                print("\t\tP_mlm(q|theta_d) = None")
            return None

        # computes the NLLR score
        query_len = len(query.split())
        left_sum, right_sum = 0, 0
        for t, p_t_theta_d in term_probs.items():
            if p_t_theta_d == 0:  # Skips the term if it is not in the collection
                continue
            query_tf = query.split().count(t)
            p_t_C = self.__term_collec_prob(t, field_weights)
            p_t_q = query_tf / query_len
            left_sum += p_t_q * math.log(p_t_theta_d)
            right_sum += p_t_q * math.log(p_t_C)
            if self.DEBUG:
                print("\tP(\"" + t + "\"|d) =", p_t_theta_d, "\tP(\"" + t + "\"|C) =", p_t_C, "\tp(\"" + t + "\"|q) =", p_t_q)
        nllr_q_d = left_sum - right_sum
        if self.DEBUG:
            print("\t\tNLLR(" + query + "|theta_d) = " + str(nllr_q_d))
        return nllr_q_d

    def __term_collec_prob(self, term, fields):
        """
        Computes term collection probability for NLLR: P(t|C) =  \sum_{f} \mu_f * P(t|C_f)

        :param term: string
        :param fields:  dictionary {field: weight, ...}
        :return: probability P(t|C)
        """
        p_t_C = 0
        for f, mu_f in fields.items():
            len_C_f = self.__elastic.coll_length(f)
            tf_t_C_f = self.__elastic.coll_term_freq(term, f)
            p_t_C += mu_f * (tf_t_C_f / len_C_f)
        return p_t_C

