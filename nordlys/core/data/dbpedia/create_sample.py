"""
create_sample
-------------

Samples a set of entities from the (raw) DBpedia collection.

Usage:

nordlys.data.dbpedia.create_sample <path_to_dbpedia> <entities_file> <output_dir>

  - path_to_dbpedia_dump: path to DBpedia dump (e.g., .../dbpedia-2015-10)
  - entities_file: file with the set of entities to be included in the sample (one entity URI per line)
  - output_dir: sample will be placed in this directory (e.g., .../dbpedia-2015-10-sample/)

@author Krisztian Balog
@author Natalia Shepeleva
"""


import os
import argparse
from rdflib.plugins.parsers.ntriples import NTriplesParser
from rdflib.plugins.parsers.ntriples import ParseError
from nordlys.core.storage.nt2mongo import Triple
from nordlys.core.storage.parser.uri_prefix import URIPrefix
from nordlys.core.utils.file_utils import FileUtils


class CreateDBpediaSample(object):

    def __init__(self, path_to_dbpedia, entities_file, output_dir):
        self.path_to_dbpedia = path_to_dbpedia
        self.entities_file = entities_file
        self.output_dir = output_dir
        self.sample_entities = []
        self.prefix = URIPrefix()

    def __load_sample_entities(self):
        """Loads the set of entities to be sampled from file."""
        self.sample_entities = FileUtils.read_file_as_list(self.entities_file)

    def __sample_file(self, dir, file):
        """Creates a local from a specific file in a given directory.

        :param dir: directory (relative to path_to_dbpedia)
        :param file:
        """
        t = Triple()
        p = NTriplesParser(t)
        infile = os.path.join(self.path_to_dbpedia, dir, file)
        outfile = os.path.join(self.output_dir, dir, file)
        print("Processing file " + file + " ...")
        i = 0
        with FileUtils.open_file_by_type(infile) as fin:
            fout = FileUtils.open_file_by_type(outfile, mode="w")  # output file will be of the same type as the input
            for line in fin:
                try:
                    p.parsestring(line.decode("utf-8"))
                except ParseError:  # skip lines that couldn't be parsed
                    continue
                if t.subject() is None:  # only if parsed as a triple
                    continue
                subj = self.prefix.get_prefixed(t.subject())  # prefixing subject
                if subj in self.sample_entities:
                    fout.write(line)
                i += 1
                if i % 100000 == 0:
                    print(str(i // 1000) + "K lines processed")
            fout.close()

    def __sample_dir(self, dir, ext):
        """Creates a local from a specific directory.

        :param dir: directory (relative to path_to_dbpedia)
        :param ext: file extensions considered
        """
        print("Processing directory " + dir + " ...")
        # make sure the dir exists under the output directory
        outdir = os.path.join(self.output_dir, dir)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        # make a local of each file from that directory with the given extension
        for root, dirs, files in os.walk(os.path.join(self.path_to_dbpedia, dir)):
            print(root)
            for file in files:
                if file.endswith(ext):
                    self.__sample_file(dir, file)

    def create_sample(self):
        """Creates a local."""
        self.__load_sample_entities()
        self.__sample_dir("core-i18n/en/", ".ttl.bz2")
        self.__sample_dir("links/", ".nt.bz2")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_dbpedia", help="path to DBpedia dump (e.g., .../dbpedia-2015-10)")
    parser.add_argument("entities_file", help="file with the set of entities to be included in the local")
    parser.add_argument("output_dir", help="local will be placed in this directory")
    args = parser.parse_args()

    cds = CreateDBpediaSample(args.path_to_dbpedia, args.entities_file, args.output_dir)
    cds.create_sample()

if __name__ == "__main__":
    main()