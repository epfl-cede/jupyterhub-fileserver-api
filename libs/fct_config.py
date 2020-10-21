import json

class ConfigFile():
    def __init__(self,filename):
        self.configjson=json.load(open(filename))
        self.auth=self.configjson['auth']
        self.ttl=self.configjson['ttl']
        self.homeroot=self.configjson['root']
        self.allget=self.configjson['allget']
