import json
import os
import logging


class ConfigFile:
    def __init__(self, filename):
        self.auth = ""
        self.ttl = 30
        self.homeroot = ""
        self.apikey = None
        config_file_present = False
        try:
            # TODO: path to config file
            self.configjson = json.load(open(filename))
            config_file_present = True
        except FileNotFoundError:
            logging.debug("No config file found")
            pass

        if config_file_present:
            self.auth = self.configjson["auth"]
            self.ttl = self.configjson["ttl"]
            self.homeroot = self.configjson["root"]
            self.allget = False  # self.configjson['allget']

        # Overwrite configuration if environment variables are set
        self.auth = os.getenv("AUTH", self.auth)
        self.homeroot = os.getenv("HOMEROOT", self.homeroot)
        self.ttl = int(os.getenv("TTL", self.ttl))
        self.apikey = os.getenv("APIKEY", self.apikey)
