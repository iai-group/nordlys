"""
DBpedia Types Indexer
=====================

Builds a DBpedia type index from entity abstracts.

The index is build directly from DBpedia files in .ttl.bz2 format (i.e., MongoDB
is not needed).

Usage
-----

::

  python -m nordlys.core.dbpedia.indexer_dbpedia_types -c <config_file>


Config parameters
------------------

- **index_name**: name of the index
- **dbpedia_files_path**: path to DBpedia .ttl.bz2 files


:Authors: Krisztian Balog, Dario Garigliotti
"""

import os
import argparse
from collections import defaultdict
from random import sample
from math import floor

from rdflib.plugins.parsers.ntriples import NTriplesParser
from rdflib.plugins.parsers.ntriples import ParseError
from rdflib.term import URIRef
from nordlys.core.storage.parser.nt_parser import Triple
from nordlys.core.storage.parser.uri_prefix import URIPrefix
from nordlys.core.utils.file_utils import FileUtils
from nordlys.core.retrieval.elastic import Elastic
from nordlys.config import DATA_DIR
from nordlys.config import PLOGGER

ENTITY_ABSTRACTS_FILE = "short_abstracts_en.ttl.bz2"
# Note that instance_types_en.ttl contains only the most specific types, while
# instance_types_transitive_en.ttl contains only the path to the path to the
# most specific types.  Therefore, both files need to be loaded.
ENTITY_TYPES_FILES = ["instance_types_en.ttl.bz2",
                      "instance_types_transitive_en.ttl.bz2"]

MAX_BULKING_DOC_SIZE = 20000000  # Max doc len when bulking, in chars (20MB)
AVG_SHORT_ABSTRACT_LEN = 216  # Based on DBpedia-2015-10


class IndexerDBpediaTypes(object):
    __DOC_TYPE = "doc"  # we don't make use of types
    __MAPPINGS = {
        "id": Elastic.notanalyzed_field(),
        "content": Elastic.analyzed_field(),
    }

    def __init__(self, config):
        self.__elastic = None
        self.__config = config
        self.__index_name = config["index_name"]
        self.__dbpedia_path = config["dbpedia_files_path"]
        # For triple parsing
        self.__prefix = URIPrefix()
        self.__triple = Triple()
        self.__ntparser = NTriplesParser(self.__triple)
        # Entity abstract and type assignments kept in memory
        self.__entity_abstracts = {}
        self.__load_entity_abstracts()
        self.__types_entities = defaultdict(list)
        self.__load_entity_types()

    @property
    def name(self):
        return self.__index_name

    def __parse_line(self, line):
        """Parses a line from a ttl file and returns subject and object pair.

        It is used for parsing DBpedia abstracts and entity types.
        The subject is always prefixed.
        For object URIs, it is returned prefixed if from DBpedia otherwise
        None (i.e., types); literal objects are always returned (i.e.,
        abstracts).
        """
        line = line.decode("utf-8") if isinstance(line, bytes) else line
        try:
            self.__ntparser.parsestring(line)
        except ParseError:  # skip lines that couldn't be parsed
            return None, None
        if self.__triple.subject() is None:  # only if parsed as a triple
            return None, None

        subj = self.__prefix.get_prefixed(self.__triple.subject())
        obj = None
        if type(self.__triple.object()) is URIRef:
            if self.__triple.object().startswith("http://dbpedia.org/ontology"):
                obj = self.__prefix.get_prefixed(self.__triple.object())
        else:
            obj = self.__triple.object().encode("utf-8")

        return subj, obj

    def __load_entity_abstracts(self):
        num_lines = 0
        filename = os.sep.join([self.__dbpedia_path, ENTITY_ABSTRACTS_FILE])
        PLOGGER.info("Loading entity abstracts from {}".format(filename))
        for line in FileUtils.read_file_as_list(filename):
            entity, abstract = self.__parse_line(line)
            if abstract and len(abstract) > 0:  # skip empty objects
                self.__entity_abstracts[entity] = abstract

            num_lines += 1
            if num_lines % 10000 == 0:
                PLOGGER.info("  {}K lines processed".format(num_lines // 1000))

        PLOGGER.info("  Done.")

    def __load_entity_types(self):
        num_lines = 0
        for types_file in ENTITY_TYPES_FILES:
            filename = os.sep.join([self.__dbpedia_path, types_file])
            PLOGGER.info("Loading entity types from {}".format(filename))
            for line in FileUtils.read_file_as_list(filename):
                entity, entity_type = self.__parse_line(line)
                if type(entity_type) != str:  # Likely result of parsing error
                    continue
                if not entity_type.startswith("<dbo:"):
                    PLOGGER.info("  Non-DBpedia type: {}".format(entity_type))
                    continue
                if not entity.startswith("<dbpedia:"):
                    PLOGGER.info("  Invalid entity: {}".format(entity))
                    continue
                self.__types_entities[entity_type].append(entity)

                num_lines += 1
                if num_lines % 10000 == 0:
                    PLOGGER.info("  {}K lines processed".format(num_lines // 1000))
            PLOGGER.info("  Done.")

    def __make_type_doc(self, type_name):
        """Gets the document representation of a type to be indexed, from its
        entity short abstracts."""
        content = "\n".join(
            [self.__entity_abstracts.get(e, b"").decode("utf-8") for e in
             self.__types_entities[type_name]])

        if len(content) > MAX_BULKING_DOC_SIZE:
            PLOGGER.info(
                "Type {} has content larger than allowed: {}.".format(
                    type_name, len(content)))

            # we randomly sample a subset of Y entity abstracts, s.t.
            # Y * AVG_SHORT_ABSTRACT_LEN <= MAX_BULKING_DOC_SIZE
            num_entities = len(self.__types_entities[type_name])
            amount_abstracts_to_sample = min(
                floor(MAX_BULKING_DOC_SIZE / AVG_SHORT_ABSTRACT_LEN),
                num_entities)
            entities_sample = [self.__types_entities[type_name][i]
                               for i in sample(range(num_entities),
                                               amount_abstracts_to_sample)]
            content = ""  # reset content
            for entity in entities_sample:
                new_content_candidate = "\n".join([content,
                                                   self.__entity_abstracts.get(
                                                       entity, b"").decode(
                                                       "utf-8")])
                # we add an abstract only if by doing so it will not exceed
                # MAX_BULKING_DOC_SIZE
                if len(new_content_candidate) > MAX_BULKING_DOC_SIZE:
                    break
                content = new_content_candidate

        return {"content": content}

    def build_index(self, force=False):
        """Builds the index.

        Note: since DBpedia only has a few hundred types, no bulk indexing is
        needed.

        :param force: True iff it is required to overwrite the index (i.e. by
        creating it by force); False by default.
        :type force: bool
        :return:
        """
        PLOGGER.info("Building type index {}".format(self.__index_name))
        self.__elastic = Elastic(self.__index_name)
        self.__elastic.create_index(mappings=self.__MAPPINGS, force=force)

        for type_name in self.__types_entities:
            PLOGGER.info("  Adding {} ...".format(type_name))
            contents = self.__make_type_doc(type_name)
            self.__elastic.add_doc(type_name, contents)

        PLOGGER.info("  Done.")


def main(args):
    config = FileUtils.load_config(args.config)
    dbpedia_path = config.get("dbpedia_files_path", "")
    # Check DBpedia files
    PLOGGER.info("Checking needed DBpedia files under {}".format(dbpedia_path))
    for fname in [ENTITY_ABSTRACTS_FILE] + ENTITY_TYPES_FILES:
        if os.path.isfile(os.sep.join([dbpedia_path, fname])):
            PLOGGER.info("  - {}: OK".format(fname))
        else:
            PLOGGER.error("  - {}: Missing".format(fname))
            exit(1)

    indexer = IndexerDBpediaTypes(config)
    indexer.build_index(force=True)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main(arg_parser())
