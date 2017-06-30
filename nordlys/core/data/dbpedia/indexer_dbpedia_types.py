"""
DBpedia Types Indexer
=====================

Build an index of DBpedia types from entity abstracts.

:Authors: Krisztian Balog, Dario Garigliotti
"""

import os
import argparse
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


ID_KEY = "id"  # not used
CONTENT_KEY = "content"
ABSTRACTS_SEPARATOR = "\n"
DEFAULT_INDEX_NAME = "dbpedia_types"
DBO_PREFIX = "<dbo:"

BULK_LEN = 1
MAX_BULKING_DOC_SIZE = 30000000  # max doc len when bulking, in chars (recommended: 5 to 15 MB)
AVG_SHORT_ABSTRACT_LEN = 216  # according to all entities appearing in DBpedia-2015-10 entity-to-type mapping


class IndexerDBpediaTypes(object):
    __DOC_TYPE = "doc"  # we don't make use of types
    __MAPPINGS = {
        # ID_KEY: Elastic.notanalyzed_field(),
        CONTENT_KEY: Elastic.analyzed_field(),
    }

    def __init__(self, config, type2entity_file, entity_abstracts_file):
        self.__elastic = None  # the index (Elastic) object
        self.__config = config
        self.__model = config.get("model", Elastic.BM25)
        self.__index_name = "{}_{}".format(config.get("index_name", DEFAULT_INDEX_NAME), self.__model.lower())
        self.__type2entity_file = type2entity_file
        self.__entity_abstracts = {}
        self.__load_entity_abstracts(entity_abstracts_file)

    @property
    def name(self):
        return self.__index_name

    def __load_entity_abstracts(self, filename):
        prefix = URIPrefix()
        t = Triple()
        p = NTriplesParser(t)
        lines_counter = 0
        PLOGGER.info("Loading entity abstracts from {}".format(filename))
        for line in FileUtils.read_file_as_list(filename):
            # basic line parsing
            line = line.decode("utf-8") if isinstance(line, bytes) else line
            try:
                p.parsestring(line)
            except ParseError:  # skip lines that couldn't be parsed
                continue
            if t.subject() is None:  # only if parsed as a triple
                continue

            # Subject and object identification
            subj = prefix.get_prefixed(t.subject())
            obj = ""
            if type(t.object()) is URIRef:
                # PLOGGER.error("Error: it is URIRef the parsed obj")
                pass
            else:
                obj = t.object().encode("utf-8")
                if len(obj) == 0:
                    continue  # skip empty objects
            self.__entity_abstracts[subj] = obj

            lines_counter += 1
            if lines_counter % 10000 == 0:
                PLOGGER.info("\t{}K lines processed".format(lines_counter // 1000))

    def __make_type_doc(self, entities, last_type):
        """Gets the document representation of a type to be indexed, from its entity short abstracts."""
        content = ABSTRACTS_SEPARATOR.join([self.__entity_abstracts.get(e, b"").decode("utf-8")
                                            for e in entities])

        if len(content) > MAX_BULKING_DOC_SIZE:

            PLOGGER.info("Type {} has content larger than allowed: {}.".format(last_type, len(content)))

            # we randomly sample a subset of Y entity abstracts, s.t. Y * AVG_SHORT_ABSTRACT_LEN <= MAX_BULKING_DOC_SIZE
            amount_abstracts_to_sample = min(floor(MAX_BULKING_DOC_SIZE / AVG_SHORT_ABSTRACT_LEN), len(entities))
            entities_sample = [entities[i] for i in sample(range(len(entities)), amount_abstracts_to_sample)]
            content = ""  # reset content

            for entity in entities_sample:
                new_content_candidate = (content + ABSTRACTS_SEPARATOR +
                                         self.__entity_abstracts.get(entity, b"").decode("utf-8"))
                # we add an abstract only if by doing so it will not exceed MAX_BULKING_DOC_SIZE
                if len(new_content_candidate) <= MAX_BULKING_DOC_SIZE:
                    content = new_content_candidate
                else:
                    break

        return {CONTENT_KEY: content}

    def build_index(self, force=False):
        """Builds the index.

        :param force: True iff it is required to overwrite the index (i.e. by creating it by force); False by default.
        :type force: bool
        :return:
        """
        self.__elastic = Elastic(self.__index_name)
        self.__elastic.create_index(mappings=self.__MAPPINGS, force=force)
        prefix = URIPrefix()

        # For indexing types in bulk
        types_bulk = {}  # dict from type id to type(=doc)

        # process type2entity file
        last_type = None
        entities = []
        lines_counter = 0
        types_counter = 0
        with FileUtils.open_file_by_type(self.__type2entity_file) as f:
            for line in f:
                line = line.decode()  # o.w. line is made of bytes
                if not line.startswith("<"):  # bad-formed lines in dataset
                    continue
                subj, obj = line.rstrip().split()

                type = prefix.get_prefixed(subj)  # subject prefixed
                entity = prefix.get_prefixed(obj)

                # use only DBpedia Ontology native types (no bibo, foaf, schema, etc.)
                if not type.startswith(DBO_PREFIX):
                    continue

                if last_type is not None and type != last_type:
                    # moving to new type, so:
                    # create a doc for this type, with all the abstracts for its entities, and store it in a bulk
                    types_counter += 1
                    # print("\n\tFound {}-th type: {}\t\t with # of entities: {}".format(types_counter, last_type,
                    #                                                                    len(entities)))
                    types_bulk[last_type] = self.__make_type_doc(entities, last_type)
                    entities = []  # important to reset it

                    if types_counter % BULK_LEN == 0:  # index the bulk of BULK_LEN docs
                        self.__elastic.add_docs_bulk(types_bulk)
                        types_bulk.clear()  # important to reset it
                        # print("Indexing a bulk of {} docs (types)... OK.".format(BULK_LEN))

                last_type = type
                entities.append(entity)

                lines_counter += 1
                if lines_counter % 10000 == 0:
                    # print("\t{}K lines processed".format(lines_counter // 1000))
                    pass
                pass

        # index the last type
        types_counter += 1

        PLOGGER.info("\n\tFound {}-th (last) type: {}\t\t with # of entities: {}".format(types_counter, last_type,
                                                                                  len(entities)))

        types_bulk[last_type] = self.__make_type_doc(entities, last_type)
        self.__elastic.add_docs_bulk(types_bulk)  # a tiny bulk :)
        # no need to reset neither entities nor types_bulk :P
        PLOGGER.info("Indexing a bulk of {} docs (types)... OK.".format(BULK_LEN))


def main(args):
    config = FileUtils.load_config(args.config)

    type2entity_file = os.path.expanduser(os.path.join(DATA_DIR, config.get("type2entity_file", "")))
    if not os.path.isfile(type2entity_file):
        # PLOGGER.error("invalid path to type-to-entity source file: ", type2entity_file)
        exit(1)

    entity_abstracts_file = os.path.expanduser(os.path.join(DATA_DIR, config.get("entity_abstracts_file", "")))
    if not os.path.isfile(entity_abstracts_file):
        # PLOGGER.error("invalid path to entity abstracts source file: ", entity_abstracts_file)
        exit(1)

    indexer = IndexerDBpediaTypes(config, type2entity_file, entity_abstracts_file)
    indexer.build_index(force=True)
    PLOGGER.info("Index build: <{}>".format(indexer.name))


def arg_parser(description=None):
    """Returns a 2-uple with the parsed paths to the type-to-entity and entity abstracts source files."""
    default_description = "It indexes DBpedia types storing the abstracts of their respective assigning entities."
    description_str = description if description else default_description
    parser = argparse.ArgumentParser(description=description_str)

    parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main(arg_parser())
