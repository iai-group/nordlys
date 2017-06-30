"""
Dbpedia to Mongo
================

The main entry point for loading DBpedia data into MongoDB.

Parameters in the config file:
  - collection: name of collection; possible values: [dbpedia-2015-10]
  - operation: building or updating a collection; possible values: [build | append]; default: append
  - Path: path to DBpedia dump
  - files: list of files to update/build upon; if set to "all", all the files in the given path are considered.
    - filename: file name with its subdirectory, e.g. core-i18n/en/labels_en.ttl.bz2
    - reverse: if true, reverses the subject-predicate-object
    - prefix: prefix to be added to the beginning of the predicate


Usage
-----

    nordlys.core.data.dbpedia.dbpedia2mongo <config_file.json>

Example config file:
{
    "collection": "dbpedia-2015-10",
    "operation": "append",
    "path": "data/dbpedia-2015-10-sample/",
    "files": [
        {"filename": "core-i18n/en/labels_en.ttl.bz2"},
        {"filename": "core-i18n/en/short_abstracts_en.ttl.bz2"},
        {"filename": "core-i18n/en/redirects_en.ttl.bz2",
         "reverse": true},
        {"filename": "core-i18n/en/wikipedia_links_en.ttl.bz2",
         "reverse": true},
        {"filename": "links/yago_type_links.nt.bz2",
         "prefix": "yago:"}
     ]
}


:Authors: Faegheh Hasibi, Krisztian Balog
"""

import sys
import os
import argparse

from nordlys.config import MONGO_DB, MONGO_HOST, MONGO_COLLECTION_DBPEDIA
from nordlys.core.storage.nt2mongo import NTriplesToMongoDB
from nordlys.core.utils.file_utils import FileUtils
from nordlys.config import PLOGGER

# static keys of config file
KEY_COLLECTION = "collection"
KEY_OPERATION = "operation"
KEY_BUILD = "build"
KEY_APPEND = "append"
KEY_PATH = "path"
KEY_FILES = "files"
KEY_FILE_NAME = "filename"
KEY_PREFIX = "prefix"
KEY_REVERSE = "reverse"


class DBpedia2Mongo(object):

    def __init__(self, config):
        """Adds path to the DBpedia raw collection.

        :param config: directory of config file
        """
        self.__check_config(config)
        self.__collection = config[KEY_COLLECTION]
        self.__operation = config[KEY_OPERATION].lower()
        self.__path = config[KEY_PATH]
        self.__files = config[KEY_FILES]

    @staticmethod
    def __check_config(config):
        """Checks params and set default values."""
        try:
            if KEY_COLLECTION not in config:
                raise Exception(KEY_COLLECTION + " is missing")
            if KEY_OPERATION not in config:
                config[KEY_OPERATION] = KEY_APPEND
            if KEY_PATH not in config:
                raise Exception(KEY_PATH + " is missing")
            if KEY_FILES not in config:
                    raise Exception(KEY_FILES + " is missing")
            # reads all files
            existing_files = set()
            for subdir, dir, files in os.walk(config[KEY_PATH]):
                for file in files:
                    existing_files.add(os.path.join(subdir, file))
            for file in config[KEY_FILES]:
                dbpedia_file = config[KEY_PATH] + file[KEY_FILE_NAME]
                if dbpedia_file not in existing_files:
                    raise Exception(dbpedia_file + " does not exist.")
        except Exception as e:
            PLOGGER.error("Error in config file: ", e)
            sys.exit(1)

    def build_dbpedia(self):
        """Builds/updates a DBpedia collection."""
        nt = NTriplesToMongoDB(MONGO_HOST, MONGO_DB, self.__collection)
        if self.__operation == KEY_BUILD:
            nt.drop()

        for file in sorted(self.__files, key=lambda f: f['filename']):
            if file.get(KEY_REVERSE, False):
                nt.add_file(self.__path + file[KEY_FILE_NAME], reverse_triple=True, predicate_prefix="!")
            else:
                nt.add_file(self.__path + file[KEY_FILE_NAME], predicate_prefix=file.get(KEY_PREFIX, ""))


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


def main(args):
    config = FileUtils.load_config(args.config)
    dbm = DBpedia2Mongo(config)
    dbm.build_dbpedia()

if __name__ == "__main__":
    main(arg_parser())
