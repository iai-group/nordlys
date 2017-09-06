"""
Generative model for interpretation set finding

@author: Faegheh Hasibi
"""

from __future__ import division

from nordlys.core.ml.instances import Instances


class Greedy(object):

    def __init__(self, score_th):
        self.__score_th = score_th

    def disambiguate(self, inss):
        """
        Takes instances and generates set of entity linking interpretations.

        :param inss: Instances object
        :return: sets of interpretations [{mention: (en_id, score), ..}, ...]
        """
        pruned_inss = self.prune_by_score(inss)
        pruned_inss = self.prune_containment_mentions(pruned_inss)
        interpretations = self.create_interpretations(pruned_inss)
        return interpretations

    def prune_by_score(self, query_inss):
        """ prunes based on a static threshold of ranking score."""
        valid_inss = []
        for ins in query_inss.get_all():
            if ins.score >= self.__score_th:
                valid_inss.append(ins)
        return Instances(valid_inss)

    def prune_containment_mentions(self, query_inss):
        """Deletes containment mentions, if they have lower score."""
        if len(query_inss.get_all()) == 0:
            return query_inss

        valid_inss = [] #dict()  # {mention: ins}
        valid_mens = set()
        for ins in sorted(query_inss.get_all(), key=lambda item: item.score, reverse=True):
            is_contained = False
            cand_men = ins.get_property("mention")
            for men in valid_mens:
                if (cand_men != men) and ((cand_men in men) or (men in cand_men)):
                    is_contained = True
            if not is_contained:
                # valid_inss[ins.get_property("mention")] = ins
                valid_inss.append(ins)
                valid_mens.add(ins.get_property("mention"))  # @todo: This line should be fixed
        return Instances(valid_inss) #list(valid_inss.values()))

    def create_interpretations(self, query_inss):
        """
        Groups CER instances as interpretation sets.

        :return list of interpretations, where each interpretation is a dictionary {mention: (en_id, score), ..}
        """
        interpretations = [dict()]  # list of dictionaries {men: ins}
        for ins in query_inss.get_all():
            added = False
            for inter in interpretations:
                mentions = list(inter.keys())
                mentions.append(ins.get_property("mention"))
                if not self.is_overlapping(mentions):
                    inter[ins.get_property("mention")] = (ins.get_property("en_id"), ins.score)
                    added = True
            if not added:
                interpretations.append({ins.get_property("mention"): (ins.get_property("en_id"), ins.score)})
        return interpretations

    def is_overlapping(self, mentions):
        """
        Checks whether the strings of a set overlapping or not.
        i.e. if there exists a term that appears twice in the whole set.

        E.g. {"the", "music man"} is not overlapping
             {"the", "the man", "music"} is overlapping.

        NOTE: If a query is "yxxz" the mentions {"yx", "xz"} and {"yx", "x"} are overlapping.

        :param mentions: A list of strings
        :return True/False
        """
        word_list = []
        for mention in mentions:
            word_list += set(mention.split())
        if len(word_list) == len(set(word_list)):
            return False
        else:
            return True