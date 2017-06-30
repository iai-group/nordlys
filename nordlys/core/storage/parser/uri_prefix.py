"""
URI Prefixing
=============

URI prefixing.

:Author: Krisztian Balog
"""

import json
from nordlys import config

PREFIX_JSON_FILE = config.DATA_DIR + "/uri_prefix/prefixes.json"


class URIPrefix(object):
    def __init__(self, prefix_file=PREFIX_JSON_FILE):
        self.prefixes = json.load(open(prefix_file))

    def __get_prefixed(self, uri):
        """Get prefixed URI."""
        prefix = None

        # if the uri contains a # then try the uri up to #
        pos = uri.find("#")
        if pos > 0:
            urip = uri[:pos + 1]  # including trailing #
            if urip in self.prefixes:
                prefix = urip

        # try longest possible match until prefix is found
        pos = uri.rfind("/")
        # note: if pos is smaller than 10 then it's probably the / from http://
        while prefix is None and pos > 10:
            urip = uri[:pos + 1]  # including trailing /
            if urip in self.prefixes:
                prefix = urip
            pos = urip[:pos].rfind("/")

        if prefix is not None:
            return uri.replace(prefix, self.prefixes[prefix] + ":")
        else:
            return uri

    def get_prefixed(self, uri, angle_brackets=True):
        if uri[0] == "<" and uri[-1] == ">":
            pref = self.__get_prefixed(uri[1:-1])
        else:
            pref = self.__get_prefixed(uri)

        if angle_brackets:
            return "<" + pref + ">"
        else:
            return pref


def convert_txt_to_json(txt_file, json_file=PREFIX_JSON_FILE):
    """Convert prefixes txt file to json.

    This has to be done only once.
    And only in case there is no .json file, or any changes done in .txt.
    """
    prefixes = {}
    ins = open(txt_file, "r")
    for line in ins:
        prefix, uri = line.strip().split("\t", 1)
        # there might be duplicates in the txt file
        # we only consider the first appearance for each URI
        # (the txt file shipped with nordlys is ordered by
        # URI frequency, so it's reasonable)
        if not uri in prefixes:
            prefixes[uri] = prefix
    ins.close()

    # write the prefix dictionary to json    
    json.dump(prefixes, open(json_file, "wb"))


if __name__ == '__main__':
    # convert prefix txt file to json
    # convert_txt_to_json("../../data/uri_prefix/prefixes.txt")

    pre = URIPrefix()
    print(pre.get_prefixed("http://www.w3.org/2000/01/rdf-schema#label"))
    print(pre.get_prefixed("<http://dbpedia.org/resource/xxx/aaa/Audi_A4>"))
