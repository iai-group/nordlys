"""Generates URI-only DBpedia index.

@author: Faegheh Hasibi
"""
import argparse
import json
from collections import defaultdict

from nordlys.config import MONGO_COLLECTION_DBPEDIA, MONGO_HOST, MONGO_DB
from nordlys.core.data.dbpedia.indexer_dbpedia import IndexerDBpedia
from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.indexer_mongo import IndexerMongo
from nordlys.core.storage.mongo import Mongo
from nordlys.core.utils.file_utils import FileUtils


class IndexerDBpediaURI(IndexerDBpedia):
    def __init__(self, config, field_counts, collection=MONGO_COLLECTION_DBPEDIA):
        super(IndexerDBpediaURI, self).__init__(config, collection)
        self.__n = config.get("top_n_fields", 500)
        self.__field_counts = field_counts
        self.__top_fields = None

    def get_top_fields(self):
        """Gets top-n frequent fields from DBpedia
        NOTE: Rank of fields with the same frequency is equal.
              This means that there can more than one field for each rank.
        """
        print("Getting the top-n frequent DBpedia fields ...")
        sorted_fields = sorted(self.__field_counts.items(), key=lambda item: item[1], reverse=True)
        print("Number of total fields:", len(sorted_fields))

        top_fields = []
        rank, prev_count, i = 0, 0, 0
        for field, count in sorted_fields:
            if field in self._config["blacklist"]:
                continue
            # changes the rank if the count number is changed
            i += 1
            if prev_count != count:
                rank = i
            prev_count = count
            if rank > self.__n:
                break
            top_fields.append(field)
        self.__top_fields = top_fields

    def get_mappings(self):
        """Sets the mappings"""
        mappings = {Elastic.FIELD_CATCHALL: Elastic.notanalyzed_searchable_field()}
        for field in self._fsdm_fields:
            mappings[field] = Elastic.notanalyzed_searchable_field()

        self.get_top_fields()
        for field in self.__top_fields:
            mappings[field] = Elastic.notanalyzed_searchable_field()

        return mappings

    def __get_field_value(self, value, f=None):
        """Converts mongoDB field value to indexable values by resolving URIs."""
        nval = []  # holds resolved values
        for v in value:
            if v.startswith("<dbpedia:"):
                nval.append(v)
        return nval

    def get_doc_content(self, doc):
        """create the index content for a given mongo document
        Here we keep both FSDM fields and individual fields for each document.

        :param doc: a Mongo document
        :return: a document ready for indexing
        """
        # Ignores document if the ID does not start with "<dbpedia:" (just to speed up)
        doc_id = Mongo.unescape(doc[Mongo.ID_FIELD])
        if not doc_id.startswith("<dbpedia:"):
            return None

        # Ignores document if it does not have must have fields
        for f in self._config["must_have"]:
            if f not in doc:
                return None

        self._doc_content = defaultdict(list)

        for f in doc:
            # Adds content for FSDM fields
            if f.lower() in self._config["names"]:
                self._doc_content["names"] += self.__get_field_value(doc[f])

            elif f in self._config["categories"]:
                self._doc_content["categories"] += self.__get_field_value(doc[f])

            elif f in self._config["similar_entity_names"]:
                self._doc_content["similar_entity_names"] += self.__get_field_value(doc[f])

            elif f not in self._config["blacklist"]:
                if doc[f][0].startswith("<dbpedia:"):
                    self._doc_content["related_entity_names"] += self.__get_field_value(doc[f], f)
                else:
                    self._doc_content["attributes"] += self.__get_field_value(doc[f], f)

            # Adds content for each individual field
            if f in self.__top_fields:
                self._doc_content[f] += self.__get_field_value(doc[f])

        # keeps only unique phrases for each field
        # Adds everything to the catchall field
        for field in self._fsdm_fields:
            self._doc_content[field] = list(set(self._doc_content[field]))
            self._doc_content[Elastic.FIELD_CATCHALL] += self._doc_content[field]

        return self._doc_content

    def build(self):
        mappings = self.get_mappings()
        indexer = IndexerMongo(self._index_name, mappings, MONGO_COLLECTION_DBPEDIA, model=self._model)
        indexer.build(self.get_doc_content)


def compute_field_counts():
    """Reads all documents in the Mongo collection and calculates field frequencies.
        i.e. For DBpedia collection, it returns all entity fields.

    :return a dictionary of fields and their frequency
    """
    print("Counting fields ...")
    dbpedia_coll = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_DBPEDIA).find_all()
    i = 0
    field_counts = dict()
    for entity in dbpedia_coll:
        for field in entity:
            if field == Mongo.ID_FIELD:
                continue
            if field in field_counts:
                field_counts[field] += 1
            else:
                field_counts[field] = 1
        i += 1
        if i % 1000000 == 0:
            print("\t", str(int(i / 1000000)), "M entity is processed!")
    return field_counts


def main(args):
    config = FileUtils.load_config(args.config)
    if "_uri" not in config["index_name"]:
        print("index name might not be correct, please check again!")
        exit(0)

    if "fields_file" not in config:
        fields_count = compute_field_counts()
    else:
        fields_count = json.load(config["fields_file"])

    indexer = IndexerDBpediaURI(config, fields_count)

    indexer.build()
    print("Index build: " + config["index_name"])
    # indexer.create_sample_file()


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main(arg_parser())