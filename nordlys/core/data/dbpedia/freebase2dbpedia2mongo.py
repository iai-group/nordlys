"""
freebase2dbpedia2mongo
----------------------

Generates a Mongo collection for mapping Freebase IDs to DBpedia

To generate one-to-one mapping, we therefore perform the followings:
1. Only proper DBpedia entities are considered (i.e. the ones that are not redirect/disambiguation pages and have name and abstract).
2. We revert back to the DBpedia 3.9 mappings (if the Freebase ID exists there) to choose a single DBpedia entity.

Note: Even with the above pre-processing, some Freebase IDs (specifically, 560) remain that are mapped to multiple DBpedia IDs.

@author: Faegheh Hasibi
"""
import argparse
import os
from collections import defaultdict
import sys
from rdflib.plugins.parsers.ntriples import NTriplesParser, ParseError

from nordlys.config import MONGO_HOST, MONGO_DB, MONGO_COLLECTION_DBPEDIA
from nordlys.core.storage.mongo import Mongo
from nordlys.core.storage.parser.nt_parser import Triple
from nordlys.core.storage.parser.uri_prefix import URIPrefix
from nordlys.core.utils.entity_utils import EntityUtils
from nordlys.core.utils.file_utils import FileUtils


# static keys of config file
KEY_COLLECTION = "collection"
KEY_MAPPING_FILE = "mapping_file"
KEY_MAPPING_FILE_39 = "mapping_file_39"
KEY_FILE_NAME = "filename"


class Freebase2DBpedia2Mongo(object):
    def __init__(self, config):
        self.__check_config(config)
        self.__collection = config[KEY_COLLECTION]
        self.__fb2dbp_file = config[KEY_MAPPING_FILE]
        self.__fb2dbp_file_39 = config[KEY_MAPPING_FILE_39]  # used for removing duplicates
        self.__prefix = URIPrefix()
        self.__mongo_dbpedia = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_DBPEDIA)

    @staticmethod
    def __check_config(config):
        """Checks params and set default values."""
        try:
            if KEY_COLLECTION not in config:
                raise Exception(KEY_COLLECTION + " is missing")
            if KEY_MAPPING_FILE not in config:
                raise Exception(KEY_MAPPING_FILE + " is missing")
            if KEY_MAPPING_FILE_39 not in config:
                raise Exception(KEY_MAPPING_FILE_39 + " is missing")
            if not(os.path.exists(config[KEY_MAPPING_FILE])) or not(os.path.exists(config[KEY_MAPPING_FILE_39])):
                raise Exception("Mapping file path does not exist.")
        except Exception as e:
            print("Error in config file: ", e)
            sys.exit(1)
        return config

    def read_fb2dbp_file(self, is_39=False):
        """Reads the file and generates an initial mapping of Freebase to DBpedia IDs.
        Only proper DBpedia entities are considered; i.e. redirect and disambiguation pages are ignored.
        """
        fb2dbp_file = self.__fb2dbp_file_39 if is_39 else self.__fb2dbp_file
        print("Processing " + fb2dbp_file + "...")

        t = Triple()
        p = NTriplesParser(t)
        i = 0
        fb2dbp_mapping = defaultdict(set)
        with FileUtils.open_file_by_type(fb2dbp_file) as f:
            for line in f:
                try:
                    p.parsestring(line.decode("utf-8"))
                except ParseError:  # skip lines that couldn't be parsed
                    continue
                if t.subject() is None:  # only if parsed as a triple
                    continue

                # prefixing
                dbp_id = self.__prefix.get_prefixed(t.subject())
                fb_id = self.__prefix.get_prefixed(t.object())

                # if reading 3.9 file, converts ID to 2015-10 version
                if is_39:
                    dbp_id = EntityUtils.convert_39_to_201510(dbp_id)
                    fb2dbp_mapping[fb_id].add(dbp_id)

                # if reading 2015-10 file, keeps only the proper DBpedia entities
                else:
                    entity_utils = EntityUtils(self.__mongo_dbpedia.find_by_id(dbp_id))
                    if entity_utils.is_entity():
                        fb2dbp_mapping[fb_id].add(dbp_id)
                i += 1
                if i % 1000 == 0:
                    print(str(i // 1000) + "K lines are processed!")

        return fb2dbp_mapping

    def load_fb2dbp_mapping(self):
        """Checks Freebase IDs that are mapped to more than one entity and keeps only one of them."""
        mappings = defaultdict(list)
        fb2dbp_39 = self.read_fb2dbp_file(is_39=True)
        fb2dbp = self.read_fb2dbp_file()

        for fb_id, dbp_ids in fb2dbp.items():
            if len(dbp_ids) > 1:
                dbp_ids_39 = fb2dbp_39.get(fb_id, None)
                dbp_id_39 = dbp_ids_39.pop() if dbp_ids_39 else None
                if dbp_id_39 in dbp_ids:
                    mappings[fb_id].append(dbp_id_39)
                else:
                    mappings[fb_id] = list(dbp_ids)
                    print(fb_id, "3.9", dbp_id_39, "2015", dbp_ids)
            else:
                mappings[fb_id] = list(dbp_ids)

        print(len(mappings))
        return mappings

    def build_collection(self, mappings):
        """Builds Mongo collection"""
        mongo = Mongo(MONGO_HOST, MONGO_DB, self.__collection)
        mongo.drop()

        predicate = "!<owl:sameAs>"
        i = 0
        for fb_id, dbp_ids in mappings.items():
            for dbp_id in dbp_ids:
                mongo.append_set(fb_id, predicate, [dbp_id])
            i += 1
            if i % 1000 == 0:
                print(str(i // 1000) + "K entities are added!")


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


def main(args):
    config = FileUtils.load_config(args.config)
    fb2dbp2mongo = Freebase2DBpedia2Mongo(config)
    mappings = fb2dbp2mongo.load_fb2dbp_mapping()
    fb2dbp2mongo.build_collection(mappings)


if __name__ == "__main__":
    main(arg_parser())
