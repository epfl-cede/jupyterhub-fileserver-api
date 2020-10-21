import os
import json

from werkzeug.utils import secure_filename

class LoD:

    def __init__(self, conf,payload):
        try :
            root=conf.homeroot
            payload=json.loads(payload)
            userloc=secure_filename(payload['user'])
            self.root = os.path.join(root,userloc)
            self.status = "OK"
            self.errcode = 0

        except :
            self.status = "Error with payload"
            self.errcode = 500

    def _path_to_dict(self, path):
        if os.path.exists(path) :
            d = {'name': os.path.basename(path)}
            if os.path.isdir(path):
                d['type'] = "directory"
                d['children'] = [self._path_to_dict(os.path.join(path, x)) for x in os.listdir \
                    (path)]
            return d
        else :
            self.status = "Directory doesn't exist"
            self.errcode = 404
            return None
    def _getLoF(self):
        try:
            self.status = "OK"
            self.errcode = 0
            return self._path_to_dict(self.root)
        except:
            self.status = "Error reading directory"
            self.errcode = -1
            return []
    def GetPayload(self):
        return self._getLoF()

    def isok(self):

        if self.status == "OK":
            return True
        else:
            return False

    def GetStatus(self):
        status = {
            'code': self.errcode,
            'status': self.status
        }
        return status
