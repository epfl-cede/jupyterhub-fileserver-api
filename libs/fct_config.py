import json
import os
import logging


class ConfigFile:
    """
    Holds configuration information, from defaults, configuration file, or environment
    variables.
    """

    def __str__(self):
        s = """
        auth: {0}
        ttl: {1}
        homeroot: {2}
        chmod: {3}
        dynamic_root: {4}
        """.format(
            self.auth, self.ttl, self.homeroot, self.chmod, self.dynamic_root
        )
        return s

    def __init__(self, filename):
        self.auth = []
        self.ttl = 30
        self.homeroot = ""
        self.chmod = False
        self.dynamic_root = None
        self.max_depth = 10
        config_file_present = False
        try:
            # TODO: path to config file
            self.configjson = json.load(open(filename))
            config_file_present = True
        except FileNotFoundError:  # pragma: no cover
            logging.warning("No config file found")
            filename = None
            pass

        if config_file_present:
            self.auth = self.configjson["auth"]
            self.ttl = self.configjson["ttl"]
            self.homeroot = self.configjson["root"]
            self.dynamic_root = self.configjson["dynamic_root"]
            self.chmod = self.configjson["chmod"]
            self.max_depth = int(self.configjson["max_depth"])

        # Overwrite configuration if environment variables are set
        user = os.getenv("AUTH_USER")
        key = os.getenv("AUTH_KEY")
        if user is not None and key is not None:
            self.auth.append({"user": user, "key": key})
        self.homeroot = os.getenv("HOMEROOT", self.homeroot)
        self.ttl = int(os.getenv("TTL", self.ttl))

        if filename is not None:
            logging.debug("Config including file {0}: {1}".format(filename, self))
        else:
            logging.debug("Config: {0}".format(self))
