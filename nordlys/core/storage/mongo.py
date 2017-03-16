"""
mongo
-----

Tools for working with MongoDB.

@author: Krisztian Balog
@author: Faegheh Hasibi
"""

import argparse
from nordlys.config import MONGO_DB, MONGO_HOST
from pymongo import MongoClient


class Mongo(object):
    """Manages the MongoDB connection and operations."""
    ID_FIELD = "_id"

    def __init__(self, host, db, collection):
        self.__client = MongoClient(host)
        self.__db = self.__client[db]
        self.__collection = self.__db[collection]
        self.__db_name = db
        self.__collection_name = collection
        print("Connected to " + self.__db_name + "." + self.__collection_name)

    @staticmethod
    def __escape(s):
        """Escapes string (to be used as key or fieldname).
        Replaces . and $ with their unicode equivalents.
        """
        return s.replace(".", "U+002E").replace("$", "U+0024")

    @staticmethod
    def unescape(s):
        """Unescapes string."""
        return s.replace("U+002E", ".").replace("U+0024", "$")

    @staticmethod
    def unescape_doc(mdoc):
        """Unescapes document content."""
        if mdoc is None:
            return None

        doc = {}
        for f in mdoc:
            if f == Mongo.ID_FIELD:
                doc[f] = Mongo.unescape(mdoc[f])
            elif type(mdoc[f]) == list:  # for DBpedia collection
                doc[Mongo.unescape(f)] = mdoc[f]
            else:                        # for surface form collections
                doc[Mongo.unescape(f)] = {}
                for key, value in mdoc[f].items():
                    doc[Mongo.unescape(f)][Mongo.unescape(key)] = value

        return doc

    def add(self, doc_id, contents):
        """Adds a document or replaces the contents of an entire document."""
        # escaping keys for content
        c = {}
        for key, value in contents.items():
            c[self.__escape(key)] = value

        try:
            self.__collection.update({Mongo.ID_FIELD: self.__escape(doc_id)},
                                     {'$set': c},
                                     upsert=True)
        except Exception as e:
            print("\nError (doc_id: " + str(doc_id) + ")\n" + str(e))

    def set(self, doc_id, field, value):
        """Sets the value of a given document field (overwrites previously stored content)."""
        self.__collection.update({Mongo.ID_FIELD: self.__escape(doc_id)},
                                 {'$set': {self.__escape(field): value}},
                                 upsert=True)

    def append_list(self, doc_id, field, value):
        """Appends the value to a given field that stores a list.
        If the field does not exist yet, it will be created.
        The value should be a list.

        :param doc_id: document id
        :param field: field
        :param value: list, a value to be appended to the current list
        """
        self.__collection.update({Mongo.ID_FIELD: self.__escape(doc_id)},
                                 {'$push': {self.__escape(field)
                                          : {'$each': [value]}}},
                                 upsert=True)

    def append_set(self, doc_id, field, value):
        """Adds a list of values to a set.
        If the field does not exist yet, it will be created.
        The value should be a list.

        :param doc_id: document id
        :param field: field
        :param value: list, a value to be appended to the current list
        """
        try:
            self.__collection.update({Mongo.ID_FIELD: self.__escape(doc_id)},
                                     {'$addToSet': {self.__escape(field)
                                                  : {'$each': value}}},
                                     upsert=True)
        except Exception as e:
            print("\nError (doc_id: " + str(doc_id) + "), field: " + field + "\n" + str(e))

    def append_dict(self, doc_id, field, dictkey, value):
        """Appends the value to a given field that stores a dict.
        If the dictkey is already in use, the value stored there will be overwritten.

        :param doc_id: document id
        :param field: field
        :param dictkey: key in the dictionary
        :param value: value to be increased by
        """
        key = self.__escape(field) + "." + self.__escape(dictkey)
        self.__collection.update({Mongo.ID_FIELD: self.__escape(doc_id)},
                                 {'$set': {key: value}},
                                 upsert=True)

    def inc(self, doc_id, field, value):
        """Increments the value of a specified field."""
        self.__collection.update({Mongo.ID_FIELD: self.__escape(doc_id)},
                                 {'$inc': {self.__escape(field): value}},
                                 upsert=True)

    def inc_in_dict(self, doc_id, field, dictkey, value=1):
        """Increments a value that is inside a dict.

        :param doc_id: document id
        :param field: field
        :param dictkey: key in the dictionary
        :param value: value to be increased by
        """
        key = self.__escape(field) + "." + self.__escape(dictkey)
        self.__collection.update({Mongo.ID_FIELD: self.__escape(doc_id)},
                                 {'$inc': {key: value}},
                                 upsert=True)

    def find_by_id(self, doc_id):
        """Returns unescaped document content for a given document id."""
        return self.unescape_doc(self.__collection.find_one({Mongo.ID_FIELD: self.__escape(doc_id)}))

    def find_all(self, no_timeout=False):
        """Returns a Cursor instance that allows us to iterate over all documents."""
        return self.__collection.find(no_cursor_timeout=no_timeout)

    def drop(self):
        """Deletes the contents of the given collection (including indices)."""
        self.__collection.drop()
        print(self.__collection_name + " dropped")

    def get_num_docs(self):
        """Returns total number of documents in the mongo collection."""
        return self.find_all().count()


    @staticmethod
    def print_doc(doc):
        print("_id: " + doc[Mongo.ID_FIELD])
        for key, value in doc.items():
            if key == Mongo.ID_FIELD: continue  # ignore the id key
            if type(value) is list:
                print(key + ":")
                for v in value:
                    print("\t" + str(v))
            else:
                print(key + ": " + str(value))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("collection", help="name of the collection")
    parser.add_argument("doc_id", help="doc_id to be looked up")
    args = parser.parse_args()

    if args.collection:
        coll = args.collection
    if args.doc_id:
        doc_id = args.doc_id

    mongo = Mongo(MONGO_HOST, MONGO_DB, coll)

    # currently, a single operation (lookup) is supported
    res = mongo.find_by_id(doc_id)
    if res is None:
        print("Document ID " + doc_id + " cannot be found")
    else:
        mongo.print_doc(res)


if __name__ == "__main__":
    main()
