"""
Entity catalog
==============

Command line end point for entity catalog

Usage
-----

python -m nordlys.services.ec  -o <operation> -i <input>


Examples
--------

  - python -m nordlys.services.ec  -o lookup_id -i <dbpedia:Audi_A4>
  - python -m nordlys.services.ec  -o "lookup_sf_dbpedia" -i "audi a4"
  - python -m nordlys.services.ec  -o "lookup_sf_facc" -i "audi a4"
  - python -m nordlys.services.ec  -o "dbpedia2freebase" -i "<dbpedia:Audi_A4>"
  - python -m nordlys.services.ec  -o "freebase2dbpedia" -i "<fb:m.030qmx>"


:Author: Faegheh Hasibi
"""
import argparse
from pprint import pprint

from nordlys.logic.entity.entity import Entity

OPERATIONS = {"lookup_id", "lookup_sf_dbpedia", "lookup_sf_facc", "freebase2dbpedia", "dbpedia2freebase"}


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", help="Name of operation", choices=OPERATIONS)
    parser.add_argument("-i", "--input", help="input entity id/name", type=str)
    args = parser.parse_args()
    return args


def main(args):
    en = Entity()
    if args.operation == "lookup_id":
        res = en.lookup_en(args.input)
    elif args.operation == "lookup_sf_dbpedia":
        res = en.lookup_name_dbpedia(args.input)
    elif args.operation == "lookup_sf_facc":
        res = en.lookup_name_facc(args.input)
    elif args.operation == "freebase2dbpedia":
        res = en.fb_to_dbp(args.input)
    elif args.operation == "dbpedia2freebase":
        res = en.dbp_to_fb(args.input)
    pprint(res)

if __name__ == "__main__":
    main(arg_parser())
