"""
Feature
=======

Implements  a generic feature class.

Authors: Faegheh Hasibi
"""
from collections import defaultdict


class FeatureCache(object):

    def __init__(self):
        self.cache = defaultdict(dict)

    def set_feature_val(self, feature_name, key, value):
        """Adds a feature and its value to the cache.

        :param feature_name: Name of the feature
        :param key: the name of what feature is computed for (e.g., a mention, entity)
        :param value: feature value
        """
        self.cache[feature_name][key] = value

    def get_feature_val(self, feature_name, key, callback_func, *args):
        """Checks the cache and computes the feature if it does not exists"""
        if key not in self.cache.get(feature_name, {}):
            self.cache[feature_name][key] = callback_func(*args)
        return self.cache[feature_name][key]