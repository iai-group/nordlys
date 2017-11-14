"""
LTR Entity Linking Approach
===========================

Class for Learning-to-Rank entity linking approach

:Author: Faegheh Hasibi
"""
import csv
import json

from nordlys.config import PLOGGER, ELASTIC_INDICES
from nordlys.core.ml.instance import Instance
from nordlys.core.ml.instances import Instances
from nordlys.core.ml.ml import ML
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.logic.el.el_utils import is_name_entity
from nordlys.logic.el.greedy import Greedy
from nordlys.logic.entity.entity import Entity
from nordlys.logic.features.feature_cache import FeatureCache
from nordlys.logic.features.ftr_entity import FtrEntity
from nordlys.logic.features.ftr_entity_similarity import FtrEntitySimilarity
from nordlys.logic.features.ftr_mention import FtrMention
from nordlys.logic.features.ftr_entity_mention import FtrEntityMention
from nordlys.logic.query.mention import Mention
from nordlys.logic.query.query import Query


class LTR(object):
    def __init__(self, query, entity, elastic, fcache, model=None, threshold=None, cmns_th=0.1):
        self.__query = query
        self.__entity = entity
        self.__elastic = elastic
        self.__fcache = fcache
        self.__model = model
        self.__threshold = threshold
        self.__cmns_th = cmns_th

    # =========================
    # Code related to training
    # =========================
    @staticmethod
    def __check_config(config):
        """Checks config parameters and set default values."""
        must_have = ["model_file", "training_set", "ground_truth", "query_file"]
        try:
            for i in range(0,2):
                if must_have[i] not in config:
                    raise Exception(must_have[i] + "is not defined!")
            if config.get("gen_training_set", False):
                for i in range(2, 4):
                    if must_have[i] not in config:
                        raise Exception(must_have[i] + "is not defined!")
        except Exception as e:
            PLOGGER.error("Error in config file: ", e)
            exit(1)

    @staticmethod
    def train(config):
        LTR.__check_config(config)
        if config.get("gen_training_set", False):
            gt = LTR.load_yerd(config["ground_truth"])
            LTR.gen_train_set(gt, config["query_file"], config["training_set"])

        instances = Instances.from_json(config["training_set"])
        ML(config).train_model(instances)

    @staticmethod
    def load_yerd(gt_file):
        """
        Reads the Y-ERD collection and returns a dictionary.

        :param gt_file: Path to the Y-ERD collection
        :return: dictionary {(qid, query, en_id, mention) ...}
        """
        PLOGGER.info("Loading the ground truth ...")
        gt = set()
        with open(gt_file, "r") as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
            for line in reader:
                if line["entity"] == "":
                    continue
                query = Query(line["query"]).query
                mention = Query(line["mention"]).query
                gt.add((line["qid"], query, line["entity"], mention))
        return gt

    @staticmethod
    def gen_train_set(gt, query_file, train_set):
        """Trains LTR model for entity linking."""
        entity, elastic, fcache = Entity(), ElasticCache(ELASTIC_INDICES[0]), FeatureCache()
        inss = Instances()
        positive_annots = set()

        # Adds groundtruth instances (positive instances)
        PLOGGER.info("Adding groundtruth instances (positive instances) ....")
        for item in sorted(gt):  # qid, query, en_id, mention
            ltr = LTR(Query(item[1], item[0]), entity, elastic, fcache)
            ins = ltr.__gen_raw_ins(item[2], item[3])
            ins.features = ltr.get_features(ins)
            ins.target = 1
            inss.add_instance(ins)
            positive_annots.add((item[0], item[2]))

        # Adds all other instances
        PLOGGER.info("Adding all other instances (negative instances) ...")
        for qid, q in sorted(json.load(open(query_file, "r")).items()):
            PLOGGER.info("Query [" + qid + "]")
            ltr = LTR(Query(q, qid), entity, elastic, fcache)
            q_inss = ltr.get_candidate_inss()
            for ins in q_inss.get_all():
                if (qid, ins.get_property("en_id")) in positive_annots:
                    continue
                ins.target = 0
                inss.add_instance(ins)
        inss.to_json(train_set)

    # =========================
    # Code related to Linking
    # =========================
    def link(self):
        """Links the query to the entity.

        :return: dictionary [{"mention": xx, "entity": yy, "score": zz}, ...]
        """
        inss = self.rank_ens()
        linked_ens = self.disambiguate(inss)
        return linked_ens

    def get_candidate_inss(self):
        """Detects mentions and their candidate entities (with their commoness scores) and generates instances

        :return: Instances object
        """
        instances = Instances()
        for ngram in self.__query.get_ngrams():
            cand_ens = Mention(ngram, self.__entity, self.__cmns_th).get_cand_ens()
            for en_id, commonness in cand_ens.items():
                if not is_name_entity(en_id):
                    continue
                self.__fcache.set_feature_val("commonness", en_id + "_" + ngram, commonness)
                ins = self.__gen_raw_ins(en_id, ngram)
                ins.features = self.get_features(ins, cand_ens)
                instances.add_instance(ins)
        return instances

    def rank_ens(self):
        """Ranks instances according to the learned LTR model

        :param n: length of n-gram
        :return: dictionary {(dbp_uri, fb_id):commonness, ..}
        """
        if self.__model is None:
            PLOGGER.error("LTR model is not defined.")

        inss = self.get_candidate_inss()
        ML({}).apply_model(inss, self.__model)
        return inss

    def disambiguate(self, inss):
        """Performs disambiguation"""
        greedy = Greedy(self.__threshold)
        inter_sets = greedy.disambiguate(inss)

        uniq_men_en = {}
        for iset in inter_sets:
            for men, (en_id, score) in iset.items():
                uniq_men_en[(men, en_id)] = score

        linked_ens = []
        for men_en, score in uniq_men_en.items():
                linked_ens.append({"mention": men_en[0], "entity": men_en[1], "score": score})
        return linked_ens

    def get_features(self, ins, cand_ens=None):
        """Generates the features set for each instance.

        :param ins: instance object
        :param cand_ens: dictionary of candidate entities {en_id: cmns, ...}
        :return: dictionary of features {ftr_name: value, ...}
        """
        e = ins.get_property("en_id")
        m = ins.get_property("mention")
        q = ins.get_property("query")

        features = {}
        # --- entity features ---
        ftr_entity = FtrEntity(e, self.__entity)
        features["outlinks"] = self.__fcache.get_feature_val("outlinks", e, ftr_entity.outlinks)
        features["redirects"] = self.__fcache.get_feature_val("redirects", e, ftr_entity.redirects)
        # --- mention features ---
        ftr_mention = FtrMention(m, self.__entity, cand_ens)
        features["len_ratio"] = ftr_mention.len_ratio(q)
        features["len"] = ftr_mention.mention_len()
        features["matches"] = self.__fcache.get_feature_val("matches", m, ftr_mention.matches)
        # --- mention-entity features ---
        ftr_entity_mention = FtrEntityMention(e, m, self.__entity)
        key = e + "_" + m
        features["commonness"] = self.__fcache.get_feature_val("commonness", key, ftr_entity_mention.commonness)
        features["mct"] = ftr_entity_mention.mct()
        features["tcm"] = ftr_entity_mention.tcm()
        features["tem"] = ftr_entity_mention.tem()
        features["pos1"] = ftr_entity_mention.pos1()
        ftr_sim_mention = FtrEntitySimilarity(m, e, self.__elastic)
        features["sim_m"] = self.__fcache.get_feature_val("sim", key, ftr_sim_mention.lm_score)
        # --- entity-query features ---
        ftr_entity_query = FtrEntityMention(e, q, self.__entity)
        features["qct"] = ftr_entity_query.mct()
        features["tcq"] = ftr_entity_query.tcm()
        features["teq"] = ftr_entity_query.tem()
        key = e + "_" + q
        ftr_sim_query = FtrEntitySimilarity(q, e, self.__elastic)
        features["sim_q"] = self.__fcache.get_feature_val("sim", key, ftr_sim_query.lm_score)
        features["context_sim"] = self.__fcache.get_feature_val("context_sim", key, ftr_sim_query.context_sim, m)
        return features

    def __gen_raw_ins(self, en_id, mention):
        """Generates an instance without features"""
        ins_id = self.__query.qid + "_" + en_id + "_" + mention
        index = self.__query.qid.rfind("_")
        session = self.__query.qid[:index] if index != -1 else self.__query.qid

        ins = Instance(ins_id)
        ins.add_property("qid", self.__query.qid)
        ins.add_property("query", self.__query.query)
        ins.add_property("en_id", en_id)
        ins.add_property("mention", mention)
        ins.add_property("session", session)
        return ins