"""
Mongo Indexer
=============

This class is a tool for creating an index from a Mongo collection.

To use this class, you need to implement :func:`callback_get_doc_content` function.
See :mod:`~nordlys.core.data.dbpedia.indexer_fsdm` for an example usage of this class.

:Author: Faegheh Hasibi
"""
from nordlys.config import MONGO_COLLECTION_DBPEDIA, MONGO_HOST, MONGO_DB
from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.storage.mongo import Mongo
# from nordlys.core.utils.logging_utils import PLOGGER


class IndexerMongo(object):

    def __init__(self, index_name, mappings, collection, model=Elastic.BM25):
        self.__index_name = index_name
        self.__mappings = mappings
        self.__mongo = Mongo(MONGO_HOST, MONGO_DB, collection)
        self.__model = model

    def build(self, callback_get_doc_content, bulk_size=1000):
        """Builds the DBpedia index from the mongo collection.

        To speedup indexing, we index documents as a bulk.
        There is an optimum value for the bulk size; try to figure it out.

        :param callback_get_doc_content: a function that get a documet from mongo and return the content for indexing
        :param bulk_size: Number of documents to be added to the index as a bulk
        """
        # PLOGGER.info("Building " + self.__index_name + " ...")
        elastic = Elastic(self.__index_name)
        elastic.create_index(self.__mappings, model=self.__model, force=True)

        i = 0
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
                elastic.add_docs_bulk(docs)
                docs = dict()
                # PLOGGER.info(str(i / 1000) + "K documents indexed")
        # indexing the last bulk of documents
        elastic.add_docs_bulk(docs)
        # PLOGGER.info("Finished indexing (" + str(i) + " documents in total)")