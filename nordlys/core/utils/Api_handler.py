"""API key handler.

:Author: Fadwa Maatug
"""

import json, os, time


class API_Handler(object):
    """Handler for api keys"""

    def __init__(self, Api_Log_Path, limit):
        self.limit_qouta = limit
        self.api_path = "{0}/api_keys.json".format(Api_Log_Path)  # holds API key-qouta file path
        with open(self.api_path) as json_file:  # loading the API key-qouta file
            self.api_file = json.load(json_file)
        with open("config/api.json") as json_file:  # loading the API config file
            self.host_file = json.load(json_file)

    def func_handler(self, api_key, ip_address):
        if self.host_file["host"] != ip_address:  # check the request IP address, and the IP of the config file
            return "The IP_address is not authorized."
        #       elif api_key is None:
        #           return "Api key is not specified."
        elif api_key not in self.api_file.keys():  # check if the key is registered in API key-qouta file
            return "API key is not authorized."
        elif self.api_file.get(api_key).get(
                'qouta') >= self.limit_qouta:  # check if the specific api key quota is not exceeded
            return "API quota exceeded."
        else:
            return True

    def update_api_file(self):  # update the API key-qouta file
        with open(self.api_path) as json_file:
            self.api_file = json.load(json_file)
