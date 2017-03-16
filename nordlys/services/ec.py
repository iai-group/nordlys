"""Entity catalog.

entity_catalog
--------------

Supports lookup functionality by ID or name.

@author: Faegheh Hasibi
"""
import argparse
from pprint import pprint

from nordlys.logic.entity.entity import Entity

OPERATIONS = {"lookup_entity", "lookup_name"}

def arg_parser():
    parser = argparse.ArgumentParser()
    # parser.add_argument("collection", help="collection name", choices=ENTITY_COLLECTIONS)
    parser.add_argument("-o", "--operation", help="Name of operation", choices=OPERATIONS)
    parser.add_argument("-in", "--input", help="input entity id/name", type=str)
    args = parser.parse_args()
    return args

def __check_args(args):
    # todo: to be used from API
    pass

def main(args):
    # config = {Entity.COLLECTION: args.collection}
    # if args.lookup_entity:
    #     config[Entity.OPERATION] = Entity.LOOKUP_ENTITY
    #     config[Entity.PARAMETERS] = {Entity.ID: args.id}
    en = Entity()
    if args.operation == "lookup_entity":
        res = en.lookup_en(args.input)
    elif args.operation == "lookup_name":
        res = en.lookup_name_dbpedia(args.input)
        # res = en.lookup_name_facc(args.input)
    pprint(res)

if __name__ == '__main__':
    main(arg_parser())
