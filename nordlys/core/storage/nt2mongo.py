"""
NTriples to Mongo
=================

Loads NTriples RDF file into MongoDB.

Documents are identified by subject URIs.
Predicate-object values are stored as key-value pairs in a dictionary,
where object can be single-valued (string) or multi-valued (list of strings). 

- Multiple ntriple files can be added to the same collection, where they would 
  be appended to the corresponding document. 
- Empty object values are filtered out, even if they're present in the NTriples
  file (that happens, for example, with DBpedia long abstracts.)

IMPORTANT: 
- It is assumed that all triples with a given subject are grouped 
  together in the .nt file (this holds, e.g., for DBpedia)
- It is also assumed that a given predicate is present only in a single file;
  when that is not the case, the contents in the last processed file will
  overwrite the previously stored values in the given field, corresponding to 
  the predicate. If it can be a problem (e.g., DBpedia uses <rdf:type> for 
  both mapping-based types and YAGO types) then use predicate prefixing!

:Authors: Faegheh Hasibi, Krisztian Balog， Natalia Shepeleva
"""

# import logging
from rdflib.plugins.parsers.ntriples import NTriplesParser
from rdflib.plugins.parsers.ntriples import ParseError
from rdflib.term import URIRef
from nordlys.core.storage.mongo import Mongo
from nordlys.core.storage.parser.nt_parser import Triple
from nordlys.core.storage.parser.uri_prefix import URIPrefix
from nordlys.core.utils.file_utils import FileUtils
from nordlys.config import PLOGGER


class NTriplesToMongoDB(object):
    def __init__(self, host, db, collection):
        self.__mongo = Mongo(host, db, collection)
        self.__prefix = URIPrefix()
        self.__m_id = None
        self.__m_contents = None
        # logging.basicConfig(level="ERROR")  # no warnings from the rdf parser

    def _next_triple(self, subj, pred, obj):
        """Processes a triple.

          - Appends to previous triple if it's the same subject.
          - Otherwise inserts last triple and creates a new one.
        """
        if (self.__m_id is not None) and (self.__m_id == subj):
            if pred not in self.__m_contents:
                self.__m_contents[pred] = []
            self.__m_contents[pred].append(obj)
        else:
            self._write_to_mongo()
            self.__m_id = subj
            self.__m_contents = {pred: [obj]}

    def _write_to_mongo(self):
        """Writes triple (inserts or appends existing) to MongoDB collection."""
        if self.__m_id is not None:
            for field, value in self.__m_contents.items():
                self.__mongo.append_set(self.__m_id, field, value)
            # self.mongo.add(self.m_id, self.m_contents)
            self.__m_id = None
            self.__m_contents = None

    def drop(self):
        """Deletes the collection."""
        self.__mongo.drop()

    def add_file(self, filename, reverse_triple=False, predicate_prefix=None):
        """Adds contents from an NTriples file to MongoDB.

        :param filename: NTriples file.
        :param reverse_triple: if set True, the subject and object values are swapped.
        :param predicate_prefix: prefix to be added to predicates.
        :param subjects_redirecter: redirects dict.
        """
        PLOGGER.info("Processing " + filename + "...")

        t = Triple()
        p = NTriplesParser(t)
        self.__m_id = None  # document id for MongoDB -- subj
        self.__m_contents = None  # document contents for MongoDB -- pred, obj
        i = 0

        with FileUtils.open_file_by_type(filename) as f:
            for line in f:
                try:
                    p.parsestring(line.decode("utf-8"))
                except ParseError:  # skip lines that couldn't be parsed
                    continue
                if t.subject() is None:  # only if parsed as a triple
                    continue

                # subject prefixing
                subj = self.__prefix.get_prefixed(t.subject())

                # predicate prefixing
                pred = self.__prefix.get_prefixed(t.predicate())
                if predicate_prefix is not None:
                    pred = predicate_prefix + pred

                # Object prefixing
                if type(t.object()) is URIRef:
                    obj = self.__prefix.get_prefixed(t.object())
                else:
                    obj = t.object()
                    if len(obj) == 0:
                        continue  # skip empty objects

                # write or append
                if reverse_triple:  # reverse subj and obj
                    self._next_triple(obj, pred, subj)
                else:  # normal mode
                    self._next_triple(subj, pred, obj)

                i += 1
                if i % 100000 == 0:
                    PLOGGER.info(str(i // 1000) + "K lines processed from " + filename)

        # process last triple
        self._write_to_mongo()


if __name__ == "__main__":
    pass
