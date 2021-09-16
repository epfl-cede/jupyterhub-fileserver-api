import json
import os
import logging


class ConfigFile:
    def __init__(self, filename):
        self.auth = []
        self.ttl = 30
        self.homeroot = ""
        sefl.chmod = False
        config_file_present = False
        try:
            # TODO: path to config file
            self.configjson = json.load(open(filename))
            config_file_present = True
        except FileNotFoundError:  # pragma: no cover
            logging.debug("No config file found")
            pass

        if config_file_present:
            self.auth = self.configjson["auth"]
            self.ttl = self.configjson["ttl"]
            self.homeroot = self.configjson["root"]
            self.chmod = self.configjson["chmod"]

        # Overwrite configuration if environment variables are set
        user = os.getenv("AUTH_USER")
        key = os.getenv("AUTH_KEY")
        if user is not None and key is not None:
            self.auth.append({"user": user, "key": key})
        self.homeroot = os.getenv("HOMEROOT", self.homeroot)
        self.ttl = int(os.getenv("TTL", self.ttl))
