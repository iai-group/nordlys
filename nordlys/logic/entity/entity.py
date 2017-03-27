"""
entity
------

Provides access to entity catalogs (DBpedia and surface forms).

@author: Faegheh Hasibi
"""

import sys
from nordlys.config import MONGO_HOST, MONGO_DB, MONGO_COLLECTION_DBPEDIA, MONGO_COLLECTION_SF_FACC, \
    MONGO_COLLECTION_FREEBASE2DBPEDIA, MONGO_COLLECTION_SF_DBPEDIA
from nordlys.core.storage.mongo import Mongo


class Entity(object):

    def __init__(self):
        self.__coll_dbpedia = None
        self.__coll_sf_facc = None
        self.__coll_sf_dbpedia = None
        self.__coll_fb2dbp = None

    def __init_coll_dbpedia(self):
        """Makes connection to the entity (DBpedia) collection."""
        if self.__coll_dbpedia is None:
            self.__coll_dbpedia = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_DBPEDIA)

    def __init_coll_sf_facc(self):
        """Makes connection to the surface form collection."""
        if self.__coll_sf_facc is None:
            self.__coll_sf_facc = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_SF_FACC)

    def __init_coll_sf_dbpedia(self):
        """Makes connection to the surface form collection."""
        if self.__coll_sf_dbpedia is None:
            self.__coll_sf_dbpedia = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_SF_DBPEDIA)

    def __init_coll_fb2dbp(self):
        """Makes connection to Freebase2DBpedia collection."""
        if self.__coll_fb2dbp is None:
            self.__coll_fb2dbp = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_FREEBASE2DBPEDIA)

    def lookup_en(self, entity_id):
        """Looks up an entity by its identifier.

        :param entity_id: entity identifier ("<dbpedia:Audi_A4>")
        :return A dictionary with the entity document or None.
        """
        self.__init_coll_dbpedia()
        return self.__coll_dbpedia.find_by_id(entity_id)

    def lookup_name_facc(self, name):
        """Looks up a name in a surface form dictionary and returns all candidate entities."""
        self.__init_coll_sf_facc()
        res = self.__coll_sf_facc.find_by_id(name)
        return res if res else {}

    def lookup_name_dbpedia(self, name):
        """Looks up a name in a surface form dictionary and returns all candidate entities."""
        self.__init_coll_sf_dbpedia()
        res = self.__coll_sf_dbpedia.find_by_id(name)
        return res if res else {}

    def fb_to_dbp(self, fb_id):
        """Converts Freebase id to DBpedia; it returns list of DBpedia IDs."""
        self.__init_coll_fb2dbp()
        res = self.__coll_fb2dbp.find_by_id(fb_id)
        return res["!<owl:sameAs>"] if res else None
