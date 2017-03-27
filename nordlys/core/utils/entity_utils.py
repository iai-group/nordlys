"""
entity_utils
----------

Utility methods for working with entities.

@author: Faegheh Hasibi
"""
from urllib.parse import unquote

from nordlys.core.storage.mongo import Mongo


class EntityUtils(object):

    PREDICATE_NAME = "<rdfs:label>"
    PREDICATE_REDIRECT = "<dbo:wikiPageRedirects>"
    PREDICATE_DISAMBIGUATE = "<dbo:wikiPageDisambiguates>"
    PREDICATE_ABSTRACT = "<dbo:abstract>"

    def __init__(self, entity):
        self.__entity = entity

    def get_id(self):
        """Returns the (internal, i.e., prefixed) URI of the entity."""
        return self.__entity[Mongo.ID_FIELD]

    def get_name(self):
        """Returns the name of a entity (or None)."""
        name = self.__entity.get(self.PREDICATE_NAME, None)
        return name[0] if name else None

    def has_name(self):
        """Checks whether the entity has a name."""
        return self.PREDICATE_NAME in self.__entity

    def has_abstract(self):
        """Checks whether the entity has abstract."""
        return self.PREDICATE_ABSTRACT in self.__entity

    def is_redirect(self):
        """Checks whether the entity is a redirect."""
        return self.PREDICATE_REDIRECT in self.__entity

    def is_disambiguation(self):
        """Checks whether the entity is a disambiguation page."""
        specified_in_url = self.get_id().endswith("_(disambiguation)>")
        has_disambiguate_predicate = self.PREDICATE_DISAMBIGUATE in self.__entity
        return specified_in_url or has_disambiguate_predicate

    def is_entity(self):
        """Checks whether the entity is a real entity.
         It means that it:
         - has a name and abstract
         - is not a disambiguation or redirect page
         """
        is_en = self.has_name() and self.has_abstract() and not(self.is_redirect()) and not(self.is_disambiguation())
        return is_en

    def has_predicate(self, predicate):
        """Checks whether the entity has the predicate."""
        return predicate in self.__entity

    def get_predicate(self, predicate):
        """Returns the values of a predicate (or None)."""
        return self.__entity.get(predicate, None)

    @staticmethod
    def convert_39_to_201510(en_id):
        """Converts DBpedia 3.9 entity IDs to 2015-10
        The encoding is based on http://wiki.dbpedia.org/uri-encoding

        :param en_id: utf-8 decoded string, e.g. <dbpedia:Karen_Sp%C3%A4rck_Jones>, <dbpedia:O_Brother,_Where_Art_Thou?>
        :return:  <dbpedia:Karen_Spärck_Jones>, <dbpedia:O_Brother,_Where_Art_Thou%3F>
        """
        special_chars = ['\"', '%', '?', '\\', '^', '`']
        encoded_chars = ['%22', '%25', '%3F', '%5C', '%5E', '%60']
        en_id = unquote(en_id)
        for i in range(0, len(special_chars)):
            en_id = en_id.replace(special_chars[i], encoded_chars[i])
        return en_id
