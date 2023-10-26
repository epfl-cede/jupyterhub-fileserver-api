import os
import time
import logging
from pathlib import Path

from libs.fct_base import RequestExecutor

log = logging.getLogger("lister")


class LoD(RequestExecutor):
    def __init__(self, conf, payload, *kwargs):
        RequestExecutor.__init__(self, conf, payload, log)
        if self.errcode != 0:
            return
        self.status = "OK"

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

    def _getLoD(self):
        try:
            self.status = "OK"
            self.errcode = 0
            return self._path_to_dict(self.user_home_path)
        except Exception as e:
            self.status = "Error reading directory: {0}".format(e)
            self.errcode = -1
            log.error("Error reading directory: {0}".format(e))
            return []

    def get_payload(self):
        return self._getLoD()


class LoF(RequestExecutor):
    def __init__(self, conf, payload, *kwargs):
        RequestExecutor.__init__(self, conf, payload, log)
        # Any exception during base class init?
        if self.errcode != 0:
            return

        try:
            self.path = self.payload["path"]
        except KeyError:
            log.error("'path' missing in payload")
            self.status = "'path' missing in payload"
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
            d = sorted(d, key=lambda x: x["name"])
            # Sort by type
            d = sorted(d, key=lambda x: x["type"])
            return d
        else:
            self.status = "Directory doesn't exist: {0}".format(path)
            self.errcode = 404
            return None

    def _getLoF(self):
        try:
            self.status = "OK"
            self.errcode = 0
            return self._path_to_dict(os.path.join(self.user_home_path, self.path))
        except Exception as e:
            self.status = "Error reading directory: {0}".format(e)
            self.errcode = -1
            log.error("Error reading directory: {0}".format(e))
            return []

    def get_payload(self):
        return self._getLoF()


class Ls(RequestExecutor):
    def __init__(self, conf, payload, *kwargs):
        RequestExecutor.__init__(self, conf, payload, log)
        # Any exception during base class init?
        if self.errcode != 0:
            return

        try:
            self.path = self.payload["path"]
        except KeyError:
            log.error("'path' missing in payload")
            self.status = "'path' missing in payload"
            self.errcode = 500
        self.root = os.path.join(self.user_home_path, self.path)

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
            d = sorted(d, key=lambda x: x["name"])
            # Sort by type
            d = sorted(d, key=lambda x: x["type"])
            return d
        else:
            log.error("Directory doesn't exist: {0}".format(path))
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
            log.error("Error reading directory: {0}".format(e))
            return []

    def get_payload(self):
        return self._getLs()
