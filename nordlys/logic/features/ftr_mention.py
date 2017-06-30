"""
FTR Mention
===========

Implements mention feature.

:Author: Krisztian Balog
"""

from nordlys.features.feature import Feature


class FtrMention(object):

    def __init__(self):
        pass

    def len_ratio(self, m, q):
        """Computes mention to query length.

        :param m: mention
        :type m: string
        :param q: query
        :type q: string
        :return:
        """
        return len(m) / len(q)
