"""NTriples parser with URI prefixing

@author: Krisztian Balog
"""

import sys
import logging
from nordlys.core.storage.parser.uri_prefix import URIPrefix
from rdflib.plugins.parsers.ntriples import NTriplesParser
from rdflib.term import URIRef


class Triple(object):
    """Representation of a Triple to be used by the rdflib NTriplesParser."""
    
    def __init__(self, prefix=None):
        self.__s = None
        self.__p = None
        self.__o = None
        self.__prefix = prefix
    
    def triple(self, s, p, o):
        """Assign current triple object

        :param s: subject
        :param p: predicate
        :param o: object
        """
        self.__s = s
        self.__p = p
        self.__o = o

    def __prefix_uri(self, uri):
        """Prefix URI and enclose in between <>

        :param uri: prefix uri
        :return: same uri, but enclosed in between <>
        """
        if self.__prefix is None:
            raise Exception("Prefix handler is not set!")
        return "<" + self.__prefix.get_prefixed(uri) + ">"

    def subject(self):
        return self.__s
    
    def subject_prefixed(self):
        return self.__prefix_uri(self.__s)
    
    def predicate(self):
        return self.__p

    def predicate_prefixed(self):
        return self.__prefix_uri(self.__p)
    
    def object(self):
        return self.__o

    def object_prefixed(self):
        if type(self.__o) is URIRef:  # only URI objects
            return self.__prefix_uri(self.__o)
        return self.__o


class TripleHandler(object):
    """This is an abstract class"""
    
    def triple_parsed(self, triple):
        """This method is called each time a triple is parsed,
        with the triple as parameter."""
        pass
    
            
class NTParser(object):
    """NTriples parser class"""
    
    def __init__(self):
        logging.basicConfig(level="ERROR")  # no warnings from the rdf parser

    def parse_file(self, filename, triplehandler):
        """Parses file and calls callback function with the parsed triple""" 
        print("Processing " + filename + "...")
        
        prefix = URIPrefix()
        t = Triple(prefix)
        p = NTriplesParser(t)    
        i = 0
        
        with open(filename) as f:
            for line in f:                
                p.parsestring(line)
                if t.subject() is None: # only if parsed as a triple
                    continue
                
                # call the handler object with the parsed triple
                triplehandler.triple_parsed(t)
                                
                i += 1
                if i % 10000 == 0: 
                    print(str(i / 1000) + "K lines processed")


class TripleHandlerPrinter(TripleHandler):
    """Example triple handler that only prints whatever it received."""
    
    def triple_parsed(self, triple):
        print("S: " + triple.subject() + " ==> " + triple.subject_prefixed())
        print("  P: " + triple.predicate() + " ==> " + triple.predicate_prefixed())
        print("  O: " + triple.object() + " ==> " + triple.object_prefixed())


def main(argv): 
    parser = NTParser()
    thp = TripleHandlerPrinter()
    parser.parse_file("/scratch/data/dbpedia-3.9/labels_en.nt", thp)
        
if __name__ == "__main__":
    main(sys.argv[1:])
            