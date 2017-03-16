"""
facc2mongo
----------

Adds entity surface forms from the Freebase Annotated ClueWeb Corpora (FACC).

The input to this script is (name variant, Freebase entity, count) triples.
See `data/facc1/README.md` for the preparation of FACC data in such format.

@author: Krisztian Balog
@author: Faegheh Hasibi
"""

import argparse
import os
import sys

from nordlys.config import MONGO_HOST, MONGO_DB, MONGO_COLLECTION_SF_FACC
from nordlys.core.storage.mongo import Mongo
from nordlys.core.utils.file_utils import FileUtils

# static key values
KEY_COLLECTION = "collection"
KEY_PATH = "path"
KEY_PREDICATE = "predicate"
KEY_LOWERCASE = "lowercase"


class FACCToMongo(object):

    def __init__(self, config):
        """Inserts FACC surface forms to Mongo."""
        self.__check_config(config)
        self.__collection = config[KEY_COLLECTION]
        self.__path = config[KEY_PATH]
        self.__predicate = config[KEY_PREDICATE]
        self.__lowercase = config[KEY_LOWERCASE]
        self.__mongo = None

    @staticmethod
    def __check_config(config):
        """Checks config parameters and sets default values."""
        try:
            if KEY_COLLECTION not in config:
                raise Exception(KEY_COLLECTION + " is missing")
            if KEY_PATH not in config:
                raise Exception(KEY_PATH + " is missing")
            if KEY_PREDICATE not in config:
                raise Exception(KEY_PREDICATE + " is missing")
            if KEY_LOWERCASE not in config:
                config[KEY_LOWERCASE] = True
        except Exception as e:
            print("Error in config file: ", e)
            sys.exit(1)

    def __add_surface_form(self, surface_form, freebase_uri, count):
        """Adds a surface form."""
        if self.__lowercase:
            surface_form = surface_form.lower()
        # Increases count; if the id is not associated with the surface form yet, it adds it with count.
        freebase_id = self.__convert_to_fb_id(freebase_uri)
        self.__mongo.inc_in_dict(surface_form, self.__predicate, freebase_id, count)

    def __convert_to_fb_id(self, fb_uri):
        """Converts /m/047b9p0 to <fb:m.047b9p0>"""
        fb_id = fb_uri.replace("/", ".")
        return "<fb:" + fb_id[1:] + ">"

    def __add_file(self, tsv_filename):
        """Adds name variants from an FACC tsv file."""
        print("Adding name variants from '" + tsv_filename + "'...")
        infile = open(tsv_filename, "r")
        for line in infile:
            f = line.rstrip().split("\t")
            self.__add_surface_form(f[0], f[1], int(f[2]))
        infile.close()

    def build(self):
        """Builds surface form collection from FACC annotations."""
        self.__mongo = Mongo(MONGO_HOST, MONGO_DB, self.__collection)
        self.__mongo.drop()

        for path, dirs, files in os.walk(self.__path):
            for fn in files:
                if fn.endswith(".tsv"):
                    self.__add_file(os.path.join(path, fn))

         
def main(args):
    config = FileUtils.load_config(args.config)
    sfm = FACCToMongo(config)
    sfm.build()


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main(arg_parser())
