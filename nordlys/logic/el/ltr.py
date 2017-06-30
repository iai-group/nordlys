"""
LTR
===

Class for Learning-to-Rank.

:Author: Krisztian Balog
"""

from nordlys.services.el.el import EL
from nordlys.query.query import Query
from nordlys.core.ml.instance import Instance
from nordlys.core.ml.instances import Instances
from nordlys.features.ftr_entity import FtrEntity
from nordlys.features.ftr_mention import FtrMention
from nordlys.features.ftr_mention_entity import FtrMentionEntity

from nordlys.core.ml.ml import ML


class LTR(object):
    def __init__(self, entity, sf, config):
        super(LTR, self).__init__(entity, sf)
        self.config = config
        self.__ml = ML({})
        self.__ftr_entity = FtrEntity(self._entity)
        self.__ftr_mention = FtrMention()
        self.__ftr_mention_entity = FtrMentionEntity(self._sf)

    def get_features(self, ins):
        e = ins.get_property("entity_id")
        m = ins.get_property("mention")
        q = ins.get_property("query")
        features = {
            'outlinks': self.__ftr_entity.outlinks(e),
            'commonness': self.__ftr_mention_entity.commonness(e, m),
            'len_ratio': self.__ftr_mention.len_ratio(m, q)
        }
        return features

    def train(self, inss, model_file=None, feat_imp_file=None):
        # for all training instances: get_features
        config = self.config
        if model_file is not None:
            config['save_model'] = model_file
        if feat_imp_file is not None:
            config['save_feature_imp'] = feat_imp_file
        self.ml.config = config
        ranker = self.ml.train_model(inss)
        return ranker

        pass

    def apply_model(self, inss, model=None):
        if model is None:  # Done for CV call_back_test method
            model = self.model
        return self.ml.apply_model(inss, model)

    def _disambiguation(self, query, cand):
        """

        :param query:
        :type query: Query
        :return:
        """
        # create instances
        inss = Instances()
        for c in cand:
            ins_id = "-".join([query.qid, "entity_id", "mention"])
            # TODO we need a 'normalized' (lowercased, special chars removed, etc.) but not fully
            # TODO prepocessed query here instead of the raw query
            prop = {'qid': query.qid,
                    'query': query.raw_query,
                    'entity_id': c['entity_id'],
                    'mention': c['mention']}
            ins = Instance(ins_id, properties=prop)
            # get features
            ins.features = self.get_features(ins)

        # apply model
        return self.apply_model(inss)
