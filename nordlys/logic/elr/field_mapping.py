"""
Field Mapping for ELR
=====================

Computes PRMS field mapping probabilities.

:Author: Faegheh Hasibi
"""

from __future__ import division
import argparse
import json
from pprint import pprint

from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.retrieval.scorer import ScorerPRMS
from nordlys.logic.elr.top_fields import TopFields


class FieldMapping(object):
    DEBUG = 0
    MAPPING_DEBUG = 0

    def __init__(self, elastic_uri, n):
        self.elastic_uri = elastic_uri
        self.n_fields = n

    def map(self, en_id):
        """
        Gets PRMS mapping probability for a clique type

        :return Dictionary {field: weight, ..}
        """
        top_fields = TopFields(self.elastic_uri).get_top_term(en_id, self.n_fields)
        scorer_prms = ScorerPRMS(self.elastic_uri, None, {'fields': top_fields})
        field_weights = scorer_prms.get_mapping_prob(en_id)
        return field_weights


def load_entities(annot_file, th=0.1):
    annots = json.load(open(annot_file, "r"))
    entities = set()
    for qid, annot in annots.items():
        for item in annot["annots"]:
            if item["score"] >= th:
                entities.add(item["entity"])
    return entities


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="json input file", type=str)
    parser.add_argument("-th", help="EL score threshold", type=float, default=0.1)
    parser.add_argument("-n", help="EL score threshold", type=int, default=10)
    args = parser.parse_args()
    return args

def main(args):
    entities = load_entities(args.input, args.th)
    mapper = FieldMapping(ElasticCache("dbpedia_2015_10_uri"), args.n)
    mappings = {}
    i = 0
    for en_id in entities:
        mappings[en_id] = mapper.map(en_id)
        i += 1
        if i % 10 == 0:
            print(i, "entities processed!")

    input_file = args.input[:args.input.rfind(".")]
    out_file = input_file + "_mapping" + ".json"
    json.dump(mappings, open(out_file, "w"), indent=4, sort_keys=True)
    print("Output file:", out_file)


if __name__ == "__main__":
    main(arg_parser())