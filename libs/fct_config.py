import json
import os


class ConfigFile:
    def __init__(self, filename):
        self.auth = ""
        self.ttl = ""
        self.homeroot = ""
        self.apikey = None
        try:
            self.configjson = json.load(open(filename))
            self.auth = self.configjson["auth"]
            self.ttl = self.configjson["ttl"]
            self.homeroot = self.configjson["root"]
            self.allget = False  # self.configjson['allget']
        except FileNotFoundError:
            pass

        # Overwrite configuration if environment variables are set
        self.auth = os.getenv("AUTH", self.auth)
        self.homeroot = os.getenv("HOMEROOT", self.homeroot)
        self.ttl = os.getenv("TTL", self.ttl)
        self.apikey = os.getenv("APIKEY", self.apikey)
