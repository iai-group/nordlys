import unittest
import numpy as np
from nordlys.config import LOGGING_PATH


def key_validate(x):
    if (len(x) < 6):
        return True


def func_manager(key):
    log_file = "{0}/api/2020-10-31.log".format(LOGGING_PATH)
    with open(log_file) as wwwlog:
        data = wwwlog.readlines()
    k_column = [line.split("key=")[1].strip() for line in data if line.find("key=") != -1]
    k_column = np.array([x for x in k_column if key_validate(x) != True])
    uniq_keys, key_count = np.unique(k_column, return_counts=True)
    keys_dict = dict(zip(uniq_keys, key_count))
    k_count = (1 for x in k_column if x == key)
    total = sum(k_count)
    return total


class Testing(unittest.TestCase):
    def test_all(self):
        self.assertEqual(func_manager('2504IG'), 38)
