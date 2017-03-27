"""
Scorer for MRF based models.
Supports FSDM and ELR-based models.

@author: Faegheh Hasibi
"""

from __future__ import division

import argparse
import json
import math
from collections import defaultdict
from pprint import pprint

from nordlys.core.ml.instance import Instance
from nordlys.core.ml.instances import Instances
from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.retrieval.scorer import ScorerPRMS
from nordlys.core.utils.entity_utils import EntityUtils
from nordlys.core.utils.file_utils import FileUtils
from nordlys.logic.elr.top_fields import TopFields


class ScorerELR(object):
    DEBUG = 0

    def __init__(self, elastic_uri, query_annot, query_len, params, n_fields=10):
        self.elastic_uri = elastic_uri
        self.query_annot = query_annot
        self.query_len = query_len
        self.n_fields = n_fields
        self.lambda_T = params[0]
        self.lambda_E = params[1]

        self.E = self.normalize_el_scores(query_annot)

    @staticmethod
    def normalize_el_scores(scores):
        """Normalize entity linking score, so that sum of all scores equal to 1"""
        normalized_scores = {}
        sum_score = sum(scores.values())
        for item, score in scores.items():
            normalized_scores[item] = score / sum_score
        return normalized_scores

    def get_field_weights(self, uri):
        """
        Gets PRMS mapping probability for a clique type

        :return Dictionary {field: weight, ..}
        """
        print("Computing field weights ...")
        # top_fields = TopFields(self.elastic_uri).get_top_term(uri, self.n_fields)
        top_fields = ["catchall"]
        scorer_prms = ScorerPRMS(self.elastic_uri, None, {'fields': top_fields})
        field_weights = scorer_prms.get_mapping_prob(uri)
        return field_weights

    def get_uri_prob(self, doc_id, field, e, lambd=0.1):
        """
        P(e|d_f) = P(e|d_f)= (1 - lambda) tf(e, d_f)+ lambda df(f, e) / df(f)

        :param doc_id: document id
        :param field: field name
        :param e: entity uri
        :param lambd: smoothing parameter
        :return: P(e|d_f)
        """
        if self.DEBUG:
            print("\t\tf:", field)
        tf = self.elastic_uri.term_freqs(doc_id, field)
        tf_e_d_f = 1 if tf.get(e, 0) > 0 else 0
        df_f_e = self.elastic_uri.doc_freq(e, field)
        df_f = self.elastic_uri.doc_count(field)
        p_e_d_f = ((1 - lambd) * tf_e_d_f) + (lambd * df_f_e / df_f)
        if self.DEBUG:
            print("\t\t\ttf(e,d_f):", tf_e_d_f, "df(f, e):", df_f_e, "df(f):", df_f, "P(e|d_f):", p_e_d_f)
        return p_e_d_f

    def get_p_e_d(self, e, field_weights, doc_id):
        """
        p(e|d) = sum_{f in F} p(e|d_f) p(f|e)

        :param e: entity URI
        :param field_weights: Dictionary {f: p_f_t, ...}
        :param doc_id: entity id
        :return p(e|d)
        """
        if self.DEBUG:
            print("\te:", e)
        p_e_d = 0
        for f, p_f_e in field_weights.items():
            p_e_d_f = self.get_uri_prob(doc_id, f, e)
            p_e_d += p_e_d_f * p_f_e
            if self.DEBUG:
                print("\t\tp(e|d_f):", p_e_d_f, "p(f|e):", p_f_e, "p(e|d_f).p(f|e):", p_e_d_f * p_f_e)
        if self.DEBUG:
            print("\tp(e|d):", p_e_d)
        return p_e_d

    def score_doc(self, doc_id, field_mappings=None):
        """
        P(q|e) = lambda_T sum_{t}P(t|d) + lambda_E sum_{e}P(e|d)

        :param doc_id: document id
        :param term_sim: term-base similarity (e.g. LM, SDM, and FSDM)
        :param: length of query
        :return: p(q|d)
        """
        if self.DEBUG:
            print("Scoring doc ID=" + doc_id)

        p_E_d = 0
        if self.lambda_E != 0:
            for e, score in self.E.items():
                field_weights = field_mappings[e] if field_mappings else self.get_field_weights(e)
                catchall_weight = {"catchall": field_weights.get("catchall", 0)}
                p_e_d = self.get_p_e_d(e, catchall_weight, doc_id)
                if p_e_d != 0:
                    p_E_d += score * math.log(p_e_d)
        return p_E_d

        # p_T_d = term_sim / self.query_len
        # p_q_d = (self.lambda_T * p_T_d) + (self.lambda_E * p_E_d)
        # if self.DEBUG:
        #     print("\t\tp(E|d):", p_E_d)
        #
        # # Adds the current doc to instances
        # # self.gen_ins(doc_id, {"p_T_d": p_T_d, "p_E_d": p_E_d})
        # return p_q_d



def load_run(run_file):
    """Loads a run file to the memory

    :param run_file: A trec run file
    :return {query: {enId: score, ..}, ...}
    """
    run = defaultdict(dict)
    with open(run_file, "r") as f:
        for line in f:
            cols = line.strip().split()
            run[cols[0]][cols[2]] = float(cols[4])
    return run


def load_annot(annot_file, th=0.1):
    """Reads TAGME annotation file and generates a dictionary

    :return {qid: {en_id: score, ..}, ..}
    """
    annots = defaultdict(dict)
    tagme_annots = json.load(open(annot_file, "r"))
    for qid, annot in tagme_annots.items():
        for item in annot["annots"]:
            if item["score"] >= th:
                en_id = item["entity"]
                annots[qid][en_id] = item["score"]
    return annots

def get_mapping_query(query_annots, mappings):
    query_mappings = {}
    for en_id in query_annots:
        query_mappings[en_id] = mappings[en_id]
    return query_mappings


def trec_format(results, query_id, run_id):
    """Outputs results in TREC format"""
    out_str = ""
    rank = 1
    for doc_id, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
        out_str += query_id + "\tQ0\t" + doc_id + "\t" + str(rank) + "\t" + str(score) + "\t" + run_id + "\n"
        rank += 1
    return out_str


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


def main(args):
    config = FileUtils.load_config(args.config)
    elastic_term = ElasticCache(config["text_index"])
    lambdas = config.get("lambdas", [0.9, 0.1])

    queries = json.load(open(config["query_file"], "r"))
    mappings = json.load(open(config["mapping_file"], "r"))
    annots = load_annot(config["annot_file"])
    run = load_run(config["run_file"])

    instances = Instances()
    # gets the results
    out_file = open(config["output_file"], "w")
    qid_int = 0
    for qid, query in sorted(queries.items()):
        print("Scoring ", qid, "...")
        results, libsvm_str = {}, ""
        query_len = len(elastic_term.analyze_query(query).split())
        scorer = ScorerELR(ElasticCache(config["uri_index"]), annots[qid], query_len, lambdas)
        for doc_id, p_T_d in sorted(run[qid].items()):
            query_mappings = get_mapping_query(annots[qid], mappings)
            p_E_d = scorer.score_doc(doc_id, query_mappings)
            properties = {'doc_id': doc_id, 'query': query, 'qid': qid, 'qid_int': qid_int}
            features = {'p_T_d': p_T_d, 'p_E_d': p_E_d}
            ins = Instance(qid + "_" + doc_id, features=features, properties=properties)
            instances.add_instance(ins)
            # libsvm_str += ins.to_libsvm(qid_prop="qod_int")
            results[doc_id] = (lambdas[0] * p_T_d) + (lambdas[1] * p_E_d)
        qid_int += 1

        # Write trec format
        out_str = trec_format(results, qid, "elr")
        out_file.write(out_str)

    out_file.close()
    print("Output file:", config["output_file"])
    instances.to_json(config["json_file"])
    print("Output file:", config["json_file"])

if __name__ == "__main__":
    main(arg_parser())
