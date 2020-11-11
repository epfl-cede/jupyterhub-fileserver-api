import os
import json
import time
from pathlib import Path

from werkzeug.utils import secure_filename

from libs.fct_global import moodle2notouser


class LoD:

    def __init__(self, conf, payload, *kwargs):
        try:
            root = conf.homeroot
            payload = json.loads(payload)
            user = moodle2notouser(payload['user'])
            if user.errcode == 0:
                userloc = user.getNotoUser()
                self.root = os.path.join(root, userloc)
                self.status = "OK"
                self.errcode = 0
            else :
                self.status = user.status
                self.errcode = user.errcode
        except:
            self.status = "Error with payload"
            self.errcode = 500

    def _path_to_dict(self, path):
        if os.path.exists(path):
            d = None
            if os.path.isdir(path):
                d = {'name': os.path.basename(path)}
                d['type'] = "directory"
                d['children'] = []
                for x in os.listdir(path):
                    if not x.startswith('.') and os.path.isdir(os.path.join(path, x)):
                        d['children'].append(self._path_to_dict(os.path.join(path, x)))
            return d
        else:
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


class Ls:

    def __init__(self, conf, payload, *kwargs):
        try:
            root = conf.homeroot
            payload = json.loads(payload)
            user = moodle2notouser(payload['user'])

            if user.errcode == 0:
                userloc = user.getNotoUser()
                path = payload['path']
                self.root = os.path.join(root, userloc, path)
                self.status = "OK"
                self.errcode = 0
            else :
                self.status = user.status
                self.errcode = user.errcode

        except:
            self.status = "Error with payload"
            self.errcode = 500

    def _path_to_dict(self, path):
        d = []
        if os.path.exists(path):
            for ls in os.listdir(path):

                if not ls.startswith('.'):  # remove hidden file
                    ls = Path(os.path.join(self.root, ls))
                    if os.path.isdir(ls):
                        d.append({'name': os.path.basename(ls), 'type': "directory"})
                    else:
                        d.append({'name': os.path.basename(ls), 'type': "file",
                                  "last-modification": time.strftime('%Y-%m-%d %H:%M:%S',
                                                                     time.localtime(ls.stat().st_mtime))})
            return d
        else:
            self.status = "Directory doesn't exist"
            self.errcode = 404
            return None

    def _getLs(self):
        try:
            self.status = "OK"
            self.errcode = 0
            return self._path_to_dict(self.root)
        except:
            self.status = "Error reading directory"
            self.errcode = -1
            return []

    def GetPayload(self):
        return self._getLs()

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
