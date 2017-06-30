"""
Dbpedia Surface Forms to Mongo
==============================

Loads Dbpedia surface forms to MongoDB.

Surface forms are extracted from the following scources:
 - Redirect pages
 - Disambiguation pages (the "(disambiguation)" part is removed from surface form)
 - Entity name (i.e. <rdfs:label> predicate)
 - Other entity names (i.e. <foaf:name> predicate)

:Authors: Faegheh Hasibi, Krisztian Balog
"""

import argparse
import sys

from nordlys.config import MONGO_DB, MONGO_HOST, MONGO_COLLECTION_DBPEDIA
from nordlys.core.storage.mongo import Mongo
from nordlys.core.utils.entity_utils import EntityUtils
from nordlys.core.utils.file_utils import FileUtils
from nordlys.config import PLOGGER


# static key values
KEY_COLLECTION = "collection"
KEY_LOWERCASE = "lowercase"


class DBpediaSurfaceforms2Mongo(object):

    def __init__(self, config):
        """Inserts DBpedia surface forms to Mongo."""
        self.__check_config(config)
        self.__collection = config[KEY_COLLECTION]
        self.__lowercase = config[KEY_LOWERCASE]
        self.__mongo_dbpedia = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_DBPEDIA)
        self.__mongo = None

    @staticmethod
    def __check_config(config):
        """Checks config parameters and sets default values."""
        try:
            if KEY_COLLECTION not in config:
                raise Exception(KEY_COLLECTION + " is missing")
            if KEY_LOWERCASE not in config:
                config[KEY_LOWERCASE] = True
        except Exception as e:
            PLOGGER.error("Error in config file: ", e)
            sys.exit(1)

    def __add_surface_form(self, surface_form, predicate, entity_id):
        """Adds a surface form (removes the disambiguation part form the surface form, if exists).

        :param surface_form: surface form for entity
        :param predicate: predicate that entity is extracted from e.g. <rdfs:label>
        :param entity_id: entity ID
        """
        if sys.getsizeof(surface_form) >= 1024:  # Mongo key limit
            return
        surface_form = surface_form.replace("(disambiguation)", "").strip()
        if self.__lowercase:
            surface_form = surface_form.lower()
        self.__mongo.inc_in_dict(surface_form, predicate, entity_id, 1)

    def build_collection(self):
        """Adds all name variants from DBpedia."""
        self.__mongo = Mongo(MONGO_HOST, MONGO_DB, self.__collection)
        self.__mongo.drop()

        # iterate through all DBpedia entities
        i = 0
        for mdoc in self.__mongo_dbpedia.find_all():
            entity = EntityUtils(Mongo.unescape_doc(mdoc))

            # skips entities without names
            if not entity.has_name():
                continue

            surface_form = entity.get_name()

            # the entity is redirect page
            if entity.is_redirect():
                entity_id = entity.get_predicate(EntityUtils.PREDICATE_REDIRECT)[0]
                self.__add_surface_form(surface_form, EntityUtils.PREDICATE_REDIRECT, entity_id)

            # the entity is disambiguation page
            if entity.has_predicate(EntityUtils.PREDICATE_DISAMBIGUATE):
                entity_ids = entity.get_predicate(EntityUtils.PREDICATE_DISAMBIGUATE)
                for entity_id in entity_ids:
                    self.__add_surface_form(surface_form, EntityUtils.PREDICATE_DISAMBIGUATE, entity_id)

            # entity is not a redirect/disambiguation page and has name and abstract
            if entity.is_entity():
                entity_id = entity.get_id()
                # adds entity name
                self.__add_surface_form(surface_form, EntityUtils.PREDICATE_NAME, entity_id)
                # adds other entity names
                foaf_name_predicate = "<foaf:name>"
                if entity.has_predicate(foaf_name_predicate):
                    for surface_form in entity.get_predicate(foaf_name_predicate):
                        self.__add_surface_form(surface_form, foaf_name_predicate, entity_id)
            i += 1
            if i % 1000 == 0:
                PLOGGER.error(str(i // 1000) + "K entities processed")

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


def main(args):
    config = FileUtils.load_config(args.config)
    dbp_sf2mongo = DBpediaSurfaceforms2Mongo(config)
    dbp_sf2mongo.build_collection()

if __name__ == "__main__":
    main(arg_parser())
