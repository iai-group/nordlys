"""
FTR Entity
==========

Implements features related to an entity.

:Author: Faegheh Hasibi
"""

IREDIRECT = "!<dbo:wikiPageRedirects>"  # Inverse Redirect
WIKILINKS = "<dbo:wikiPageWikiLink>"


class FtrEntity(object):

    def __init__(self, en_id, entity):
        self.__en_id = en_id
        self.__en_doc = entity.lookup_en(en_id)

    def redirects(self):
        """Number of redirect pages linking to the entity"""
        reds = self.__en_doc.get(IREDIRECT, [])
        return len(set(reds))

    def outlinks(self):
        """ Number of entity out-links"""
        links = self.__en_doc.get(WIKILINKS, [])
        return len(set(links))
