"""
File Utils
==========

Utility methods for file handling.

:Authors: Krisztian Balog, Faegheh Hasibi
"""

import bz2
import gzip
import json
import sys
import os.path as op


class FileUtils(object):
    @staticmethod
    def open_file_by_type(file_name, mode="r"):
        """Opens file (gz/text) and returns the handler.

        :param file_name: NTriples file
        :return: handler to the file
        """
        file_name = op.expanduser(file_name)  # expands '~' to the absolute home dir
        if file_name.endswith("bz2"):
            return bz2.open(file_name, mode)
        elif file_name.endswith("gz"):
            return gzip.open(file_name, mode, encoding="utf-8")
        else:
            return open(file_name, mode, encoding="utf-8")

    @staticmethod
    def read_file_as_list(filename):
        """Reads in non-empty lines from a textfile (which may be gzipped/bz2ed) and returns it as a list.

        :param filename:
        """
        with FileUtils.open_file_by_type(filename) as f:
            return [l for l in (line.strip() for line in f) if l]

    @staticmethod
    def load_config(config):
        """Loads config file/dictionary.

        :param config: json file or a dictionary
        :return: config dictionary
        """
        # config is a dictionary
        if type(config) == dict:
            return config

        # opens config file
        try:
            return json.load(open(op.expanduser(config)))
        except Exception as e:
            print("Error loading config file: ", e)
            sys.exit(1)

    @staticmethod
    def dump_tsv(file_name, data, header=None, append=False):
        """Dumps the data in tsv format.

        :param file_name: name of file
        :param data: list of list
        :param header: list of headers
        :param append: if True, appends the data to the existing file
        """
        mode = "a" if append else "w"
        with open(file_name, mode) as f:
            print("tsv file created:", file_name)
            if header:
                f.write("\t".join(header) + "\n")
            for line in data:
                f.write("\t".join([str(d) for d in line]) + "\n")


def main():
    header = ["c1", "c2"]
    data = [[1, 2], [3, 4]]
    FileUtils.dump_tsv("output/test.tsv", data, header)
    FileUtils.dump_tsv("output/test.tsv", [[5, 6], [7, 8]], append=True)


if __name__ == "__main__":
    main()
