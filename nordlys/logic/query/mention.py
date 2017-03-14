"""

Class for entity mentions (used for entity linking)

- Generates all candidate entities for a mention
- Computes commonness for a mention-entity pairs
"""
import sys

from nordlys.logic.entity.entity import Entity


class Mention(object):
    def __init__(self, mention, entity, cmns_th=None):
        self.__mention = mention.lower()
        self.__entity = entity
        self.__cmns_th = cmns_th

    def get_cand_ens(self):
        """Returns all candidate entities for the mention

        :return: {en:cmn_score}
        """
        all_matches = self.__entity.lookup_name_facc(self.__mention)
        facc_matches = self.__get_facc_matches(all_matches)
        cand_ens = self.__filter_uncommon_ens(facc_matches) if self.__cmns_th else facc_matches

        # todo: add dbpedia entities after rebuilding surface form dictionary
        # dbpedia_matches = self.__get_dbpedia_ens(all_matches)
        # cand_ens.update(dbpedia_matches)
        return cand_ens

    def __get_facc_matches(self, matches):
        """Returns entities matching the mention according to FACC.
        - Computes commonness for each entity (if needed)
        - Converts Freebase IDs to DBpedia
        """
        # computes the denominator for commonness
        facc_matches = matches.get("facc12", {})
        if self.__cmns_th:
            facc_matches = self.__get_commonness_scores(facc_matches)

        # converts freebased IDs to DBpedia
        facc_ens = {}
        for entity_id, val in facc_matches.items():
            dbp_ids = self.__entity.fb_to_dbp(entity_id)
            if dbp_ids is None:
                continue
            for dbp_id in dbp_ids:
                facc_ens[dbp_id] = val
        return facc_ens

    def __get_commonness_scores(self, en_counts):
        """Computes commonness score for a all entities matching the mention.

        :param en_counts: dictionary {entity_id: count, ...}
        :return: commonness scores {entity_id: commonness, ...}
        """
        commonness_scores = {}
        total_occurrences = sum(en_counts.values())
        for en, count in en_counts.items():
            commonness_scores[en] = count / total_occurrences
        return commonness_scores

    def __filter_uncommon_ens(self, en_cmns):
        """Filters out entities that are below the commonness threshold.

        :param en_cmns: dictionary {entity_id: count, ...}
        :return: filtered dictionary
        """
        filtered_ens = {}
        for en, cmns in en_cmns.items():
            if cmns >= self.__cmns_th:
                filtered_ens[en] = cmns
        return filtered_ens

    def __get_dbpedia_ens(self, matches):
        """Returns entities matching the mention according to DBpedia."""
        # todo: write the function after rebuilding sf_coll
        return {}



def main(args):
    entity = Entity()
    mention = Mention(args[0], entity, cmns_th=0.1)
    ens = mention.get_cand_ens()
    print(ens)

if __name__ == "__main__":
    main(sys.argv[1:])