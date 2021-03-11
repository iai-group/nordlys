"""
Modification of the original Mongo Indexer that generates JSON files to be
later ingested by Anserini.


To use this class, you need to implement :func:`callback_get_doc_content` function.
See :mod:`~nordlys.core.data.dbpedia.indexer_fsdm` for an example usage of this class.

:Author: Faegheh Hasibi, Krisztian Balog
"""
import json

from nordlys.config import MONGO_COLLECTION_DBPEDIA, MONGO_HOST, MONGO_DB, \
    PLOGGER
from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.storage.mongo import Mongo


# from nordlys.core.utils.logging_utils import PLOGGER


class IndexerMongo(object):

    def __init__(self, path, mappings, collection, model=Elastic.BM25):
        self.__path = path
        self.__mappings = mappings
        self.__mongo = Mongo(MONGO_HOST, MONGO_DB, collection)
        self.__model = model

    def __dump_docs_bulk(self, bulk_id, docs):
        """Dumps a bulk of indexable documents to a json file."""
        contents = [doc for _, doc in docs.items()]
        json.dump(contents,
                  open("{}/{:05d}.json".format(self.__path, bulk_id), "w"),
                  indent=4, ensure_ascii=False)

    def build(self, callback_get_doc_content, bulk_size=1000):
        """Builds the DBpedia index from the mongo collection.

        To speedup indexing, we index documents as a bulk.
        There is an optimum value for the bulk size; try to figure it out.

        :param callback_get_doc_content: a function that get a documet from mongo and return the content for indexing
        :param bulk_size: Number of documents to be added to the index as a bulk
        """
        PLOGGER.info("Dumping files to " + self.__path + " ...")

        i = 0
        bulk_id = 0
        docs = dict()
        for mdoc in self.__mongo.find_all(no_timeout=True):
            docid = Mongo.unescape(mdoc[Mongo.ID_FIELD])

            # get back document from mongo with keys and _id field unescaped
            doc = callback_get_doc_content(Mongo.unescape_doc(mdoc))
            if doc is None:
                continue
            docs[docid] = doc

            i += 1
            if i % bulk_size == 0:
                self.__dump_docs_bulk(bulk_id, docs)
                bulk_id += 1
                docs = dict()
                PLOGGER.info(str(i / 1000) + "K documents indexed")
        # indexing the last bulk of documents
        self.__dump_docs_bulk(bulk_id, docs)
        PLOGGER.info("Finished indexing (" + str(i) + " documents in total)")
