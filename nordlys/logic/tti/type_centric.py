"""
Type centric method for TTI.

@author:
"""
from nordlys.config import ELASTIC_TTI_INDICES
from nordlys.core.retrieval.elastic_cache import ElasticCache


TC_INDEX = ELASTIC_TTI_INDICES[0]

class TypeCentric(object):
    def __init__(self, query, retrieval_config):
        self.__query = query
        self.__retrieval_config = retrieval_config
        self.__elasttic = ElasticCache(TC_INDEX)

    def __type_centric(self, query):
        """Type-centric TTI."""
        types = dict()
        model = self.__config.get("model", TTI_MODEL_BM25)

        elastic = ElasticCache(self.__tc_config.get("index", DEFAULT_TTI_TC_INDEX))
        if model == TTI_MODEL_BM25:
            print("TTI, TC, BM25")
            scorer = Scorer.get_scorer(elastic, query, self.__tc_config)
            types = Retrieval(self.__tc_config).retrieve(query, scorer)

        elif model == TTI_MODEL_LM:
            print("TTI, TC, LM")
            self.__tc_config["model"] = "lm"  # Needed for 2nd-pass
            self.__tc_config["field"] = "content"  # Needed for 2nd-pass
            self.__tc_config["second_pass"] = {
                "field": "content"
            }
            for param in ["smoothing_method", "smoothing_param"]:
                if self.__config.get(param, None) is not None:
                    self.__tc_config["second_pass"][param] = self.__config.get(param)

            scorer = Scorer.get_scorer(elastic, query, self.__tc_config)
            types = Retrieval(self.__tc_config).retrieve(query, scorer)

        return types