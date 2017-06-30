"""
Late Fusion Scorer
==================

Class for late fusion scorer (i.e., document-centric model).

:Authors: Shuo Zhang, Krisztian Balog, Dario Garigliotti
"""
from nordlys.logic.fusion.fusion_scorer import FusionScorer
from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.core.retrieval.retrieval_results import RetrievalResults
from nordlys.core.retrieval.scorer import Scorer, ScorerLM
from nordlys.core.retrieval.retrieval import Retrieval


class LateFusionScorer(FusionScorer):
    def __init__(self, index_name, retr_model, retr_params, num_docs=None,
                 field="content", run_id="fusion", num_objs=100, assoc_mode=FusionScorer.ASSOC_MODE_BINARY,
                 assoc_file=None):
        """

        :param index_name: name of index
        :param assoc_file: document-object association file
        :param assoc_mode: document-object weight mode, uniform or binary
        :param retr_model: the retrieval model; valid values: "lm", "bm25"
        :param retr_params: config including smoothing method and parameter
        :param num_objs: the number of ranked objects for a query
        :param assoc_mode: the fusion weights, which could be binary or uniform
        :param assoc_file: object-doc association file
        """
        super(LateFusionScorer, self).__init__(index_name, association_file=assoc_file, run_id=run_id)
        self.__config = {
            "index_name": self._index_name,
            "first_pass": {
                "num_docs": num_docs,
                "field": field
            },
        }
        self._field = field
        self._num_docs = num_docs
        self._model = retr_model
        self._params = retr_params
        self._assoc_mode = assoc_mode
        self._num = num_objs
        self._elastic = ElasticCache(self._index_name)

    def score_query(self, query, assoc_fun=None):
        """
        Scores a given query.

        :param query: query string.
        :return: a RetrievalResults instance.
        :func assoc_fun: function to return a list of docs for an obeject
        """
        scorer = None
        # setting the configurations
        self.__config["field"] = self._field  # Needed for 2nd-pass
        self.__config["model"] = self._model  # Needed for 2nd-pass
        if self._model == "lm":
            self.__config["second_pass"] = {
                "field": self._field
            }
            for param in ["smoothing_method", "smoothing_param"]:
                if self.__config.get(param, None) is not None:
                    self.__config["second_pass"][param] = self._params.get(param, None)

            scorer = ScorerLM.get_scorer(self._elastic, query, self.__config)
        else:
            # print("LF config = {}".format(self.__config))
            # scorer = None  # scorer for default model
            pass  # TODO add the BM25 case body

        # retrieving documents
        res = Retrieval(self.__config).retrieve(query, scorer)

        # getting the doc-to-object mappings
        if assoc_fun is not None:
            for doc_id, _ in res.items():
                self.assoc_doc[doc_id] = assoc_fun(doc_id)

        # scoring objects, i.e., computing P(q|o)
        pqo = dict()
        for i, item in enumerate(list(res.keys())):
            if self._num_docs is not None and i + 1 == self._num_docs:  # consider only top documents
                break
            doc_id = item
            doc_score = res[doc_id].get("score", 0)
            if doc_id in self.assoc_doc:
                for object_id in self.assoc_doc[doc_id]:
                    if self._assoc_mode == FusionScorer.ASSOC_MODE_BINARY:
                        w_do = 1
                    elif self._assoc_mode == FusionScorer.ASSOC_MODE_UNIFORM:
                        w_do = 1 / len(self.assoc_obj[object_id])
                    else:
                        w_do = 0  # this should never happen
                    pqo[object_id] = pqo.get(object_id, 0) + doc_score * w_do

        return RetrievalResults(pqo)
