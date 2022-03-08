import os
import json
import time
from pathlib import Path

from libs.fct_global import moodle2notouser
from libs.fct_global import DynamicRoot


class LoD:
    def __init__(self, conf, payload, *kwargs):
        try:
            dyn_root = DynamicRoot(conf)
            payload = json.loads(payload)
            user = moodle2notouser(payload["user"])

            if user.errcode == 0:
                userloc = user.getNotoUser()
                if userloc == "":
                    self.status = "Empty user path rejected"
                    self.errcode = 500
                    self.root = dyn_root.getInvalidPath()
                    return
                self.root = os.path.join(dyn_root.getRoot(userloc)["root"], userloc)
                self.status = "OK"
                self.errcode = 0
            else:
                self.status = user.status
                self.errcode = user.errcode
        except Exception as e:
            self.status = "Error with payload: {0}".format(e)
            self.errcode = 500

    def _path_to_dict(self, path):
        if os.path.exists(path):
            d = None
            if os.path.isdir(path):
                d = {"name": os.path.basename(path)}
                d["type"] = "directory"
                d["children"] = []
                for x in os.listdir(path):
                    if not x.startswith(".") and os.path.isdir(os.path.join(path, x)):
                        d["children"].append(self._path_to_dict(os.path.join(path, x)))
            return d
        else:
            self.status = "Directory doesn't exist: {0}".format(path)
            self.errcode = 404
            return None

    def _getLoF(self):
        try:
            self.status = "OK"
            self.errcode = 0
            return self._path_to_dict(self.root)
        except Exception as e:
            self.status = "Error reading directory: {0}".format(e)
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
        status = {"code": self.errcode, "status": self.status}
        return status


class LoF:
    def __init__(self, conf, payload, *kwargs):
        try:
            dyn_root = DynamicRoot(conf)
            payload = json.loads(payload)
            user = moodle2notouser(payload["user"])

            if user.errcode == 0:
                userloc = user.getNotoUser()
                if userloc == "":
                    # Never return with an empty user path, would allow access to all user directories
                    self.status = "Empty user path rejected"
                    self.errcode = 500
                    self.root = dyn_root.getInvalidPath()
                    return
                self.root = os.path.join(dyn_root.getRoot(userloc)["root"], userloc)
                self.path = payload["path"]
                self.status = "OK"
                self.errcode = 0
            else:
                self.status = user.status
                self.errcode = user.errcode

        except Exception as e:
            self.status = "Error with payload: {0}".format(e)
            self.errcode = 500

    def _path_to_dict(self, path):
        d = []
        if os.path.exists(path):
            for ls in os.listdir(path):

                if not ls.startswith("."):  # remove hidden file
                    ls = Path(os.path.join(path, ls))
                    if os.path.isdir(ls):
                        d.append(
                            {
                                "name": os.path.basename(ls),
                                "type": "directory",
                                "children": self._path_to_dict(ls),
                            }
                        )
                    else:
                        try:
                            last_mod = time.strftime(
                                "%Y-%m-%d %H:%M:%S", time.localtime(ls.stat().st_mtime)
                            )
                        except:  # noqa: E722
                            last_mod = "unknown"
                        d.append(
                            {
                                "name": os.path.basename(ls),
                                "type": "file",
                                "last-modification": last_mod,
                            }
                        )
            # Sort by name
            d = sorted(d, key=lambda x: x['name'])
            # Sort by type
            d = sorted(d, key=lambda x: x['type'])
            return d
        else:
            self.status = "Directory doesn't exist: {0}".format(path)
            self.errcode = 404
            return None

    def _getLoF(self):
        try:
            self.status = "OK"
            self.errcode = 0
            return self._path_to_dict(os.path.join(self.root, self.path))
        except Exception as e:
            self.status = "Error reading directory: {0}".format(e)
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
        status = {"code": self.errcode, "status": self.status}
        return status


class Ls:
    def __init__(self, conf, payload, *kwargs):
        try:
            dyn_root = DynamicRoot(conf)
            payload = json.loads(payload)
            user = moodle2notouser(payload["user"])

            if user.errcode == 0:
                userloc = user.getNotoUser()
                if userloc == "":
                    # Never return with an empty user path, would allow access to all user directories
                    self.status = "Empty user path rejected"
                    self.errcode = 500
                    self.root = dyn_root.getInvalidPath()
                    return
                path = payload["path"]
                self.root = os.path.join(
                    dyn_root.getRoot(userloc)["root"], userloc, path
                )
                self.status = "OK"
                self.errcode = 0
            else:
                self.status = user.status
                self.errcode = user.errcode

        except Exception as e:
            self.status = "Error with payload AAA: {0}".format(e)
            self.errcode = 500

    def _path_to_dict(self, path):
        d = []
        if os.path.exists(path):
            for ls in os.listdir(path):

                if not ls.startswith("."):  # remove hidden file
                    ls = Path(os.path.join(self.root, ls))
                    if os.path.isdir(ls):
                        d.append({"name": os.path.basename(ls), "type": "directory"})
                    else:
                        d.append(
                            {
                                "name": os.path.basename(ls),
                                "type": "file",
                                "last-modification": time.strftime(
                                    "%Y-%m-%d %H:%M:%S",
                                    time.localtime(ls.stat().st_mtime),
                                ),
                            }
                        )
            # Sort by name
            d = sorted(d, key=lambda x: x['name'])
            # Sort by type
            d = sorted(d, key=lambda x: x['type'])
            return d
        else:
            self.status = "Directory doesn't exist: {0}".format(path)
            self.errcode = 404
            return None

    def _getLs(self):
        try:
            self.status = "OK"
            self.errcode = 0
            return self._path_to_dict(self.root)
        except Exception as e:
            self.status = "Error reading directory: {0}".format(e)
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
        status = {"code": self.errcode, "status": self.status}
        return status
