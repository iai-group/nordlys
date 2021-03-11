"""
Modification of the original DBpedia Indexer that generates JSON files to be
later ingested by Anserini.

The index config file should contain a 'path' key with the location of

:Author: Faegheh Hasibi, Krisztian Balog
"""
import argparse
import json
from collections import defaultdict

from nordlys.config import MONGO_HOST, MONGO_DB, MONGO_COLLECTION_DBPEDIA
from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.indexer_mongo import IndexerMongo
from nordlys.core.storage.mongo import Mongo
from nordlys.core.utils.file_utils import FileUtils
from nordlys.config import PLOGGER


class IndexerDBpedia(object):
    def __init__(self, config, collection=MONGO_COLLECTION_DBPEDIA):
        self._config = config
        self._path = config["path"]
        self._model = config.get("model", Elastic.BM25)
        self._collection = collection
        self._doc_content = defaultdict(list)
        self._fsdm_fields = ["names", "categories", "attributes", "similar_entity_names", "related_entity_names"]

    def get_mappings(self):
        """Sets the mappings"""
        mappings = {Elastic.FIELD_CATCHALL: Elastic.analyzed_field()}
        mappings["abstract"] = Elastic.analyzed_field()
        for field in self._fsdm_fields:
            mappings[field] = Elastic.analyzed_field()
        return mappings

    def _is_uri(self, value):
        """Returns true if the value is uri. """
        if value.startswith("<") and value.endswith(">"):
            return True
        return False

    def __resolve_uri(self, uri):
        """Resolves the URI using a simple heuristic."""
        if self._is_uri(uri):
            if uri.startswith("<dbpedia:Category") or uri.startswith("<dbpedia:File"):
                return uri[uri.rfind(":") + 1:-1].replace("_", " ")
            elif uri.startswith("<http://en.wikipedia.org"):
                return uri[uri.rfind("/") + 1:-1].replace("_", " ")
            elif not uri.startswith("<http"):  # for <dbpedia:XXX>
                return uri[uri.find(":") + 1:-1].replace("_", " ")
        return uri.replace("<", "").replace(">", "")

    def __resolve_field(self, f):
        """Returns resolved field names."""
        f = self.__resolve_uri(f)
        f_name = ""
        for char in f:
            f_name += char if not char.isupper() else " " + char
        return f_name

    def __get_field_value(self, value, f=None):
        """Converts mongoDB field value to indexable values by resolving URIs."""
        nval = []  # holds resolved values
        for v in value:
            v = str(v)
            v = self.__resolve_uri(v) if self._is_uri(v) else v
            v = self.__resolve_field(f) + " " + v if (f is not None) and (f.startswith("<dbp")) else v
            nval.append(v)
        return nval

    def get_doc_content(self, doc):
        """create the index content for a given mongo document

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
            # Adds content to FSDM fields
            if f.lower() in self._config["names"]:
                self._doc_content["names"] += self.__get_field_value(doc[f])

            elif f in self._config["categories"]:
                self._doc_content["categories"] += self.__get_field_value(doc[f])

            elif f in self._config["similar_entity_names"]:
                self._doc_content["similar_entity_names"] += self.__get_field_value(doc[f])

            elif f not in self._config["blacklist"]:
                if self._is_uri(doc[f][0]): #doc[f][0].startswith("<dbpedia:"):
                    self._doc_content["related_entity_names"] += self.__get_field_value(doc[f], f)
                else:
                    self._doc_content["attributes"] += self.__get_field_value(doc[f], f)

        # keeps only unique phrases for each field
        # Adds everything to the catchall field
        for field in self._fsdm_fields:
            self._doc_content[field] = list(set(self._doc_content[field]))
            self._doc_content[Elastic.FIELD_CATCHALL] += self._doc_content[field]

        # Generates an abstract field
        self._doc_content["abstract"] = doc["<rdfs:comment>"][0]

        return self._doc_content

    def build(self):
        mappings = self.get_mappings()
        indexer = IndexerMongo(self._path, mappings, MONGO_COLLECTION_DBPEDIA, model=self._model)
        indexer.build(self.get_doc_content)

    def create_sample_file(self):
        """Creates a sample file from the context of index"""
        mongo = Mongo(MONGO_HOST, MONGO_DB, MONGO_COLLECTION_DBPEDIA)

        example_docs = ["<dbpedia:Texhoma,_Oklahoma>", "<dbpedia:Karen_Spärck_Jones>",
                        "<dbpedia:Audi_A4>", "<dbpedia:Barack_Obama>"]
        doc_contents = {}
        for docid in example_docs:
            doc_contents[docid] = self.get_doc_content(mongo.find_by_id(docid))
        json.dump(doc_contents, open("output/example_docs.json", "w"), indent=4, sort_keys=True, ensure_ascii=False)


def main(args):
    config = FileUtils.load_config(args.config)
    indexer = IndexerDBpedia(config)
    indexer.build()
    PLOGGER.info("Indexable files dumped: " + config["path"])
    # indexer.create_sample_file()


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main(arg_parser())
