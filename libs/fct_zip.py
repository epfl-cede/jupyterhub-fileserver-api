from io import BytesIO
import zipfile
import os
import json
import base64

from libs.fct_global import moodle2notouser, SendLog, DynamicRoot


class ZipBlob:
    """
    Manage zip file from and to blob base64
    """

    def GetZip(self, path):
        """
        return a base 64 blob zip of all the content of path
        :param path: path of the zip
        :return: base 64 blob of zip
        """
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    archivepath = filepath.replace(path, "")
                    zipf.write(filepath, archivepath)
        memory_file.seek(0)
        return base64.b64encode(memory_file.read()).decode("utf-8")

    def PutZip(self, blob, path):
        memory_file = BytesIO(blob.read())  # BytesIO(base64.b64decode(blob))
        with zipfile.ZipFile(memory_file, "r") as zipf:
            os.chdir(path)
            zipf.extractall()


class ZfS:
    """
    This class is called for downloading a Zip from a given directory
    """

    def __init__(self, conf, payload, *kwargs):
        sl = SendLog()
        sl.write(event="ZfS", action="init", userid=None)
        try:
            # root = conf.homeroot
            dyn_root = DynamicRoot(conf)
            payload = json.loads(payload)
            self.user = moodle2notouser(payload["user"])

            if self.user.errcode == 0:
                userloc = self.user.getNotoUser()
                folder = payload["folder"]
                # self.root = os.path.join(root, userloc, folder)
                self.root = os.path.join(
                    dyn_root.getRoot(userloc)["root"], userloc, folder
                )
                self.origin = os.path.join(userloc, folder)
                sl.write(event="self.root", action=self.root, userid=None)
                if not os.path.exists(self.root):
                    self.status = "Error : destination does not exist"
                    self.errcode = 440
                else:
                    self.status = "OK"
                    self.errcode = 0
            else:
                self.status = self.user.status
                self.errcode = self.user.errcode

        except Exception as e:
            self.status = "Error with payload: {0}".format(e)
            self.errcode = 500

    def _getZfS(self):
        log = SendLog()
        try:
            self.status = "OK"
            self.errcode = 0
            zip = ZipBlob()
            blob = zip.GetZip(self.root)
            log.write("Zfs SUCCESS", "from : " + self.root, self.user.getNotoUserid())
            return {
                "origin": self.origin,
                "blob": blob,
                "method": "base64",
                "mime": "application/zip",
            }
        except Exception as e:
            self.status = "Error: zip is not working in this directory: {0}".format(e)
            self.errcode = -1
            log.write("Zfs FAILED", "from : " + self.root, self.user.getNotoUserid())
            return []

    def GetPayload(self):
        return self._getZfS()

    def isok(self):

        if self.status == "OK":
            return True
        else:
            return False

    def GetStatus(self):
        status = {"code": self.errcode, "status": self.status}
        return status


class UzU:
    """
    This class is called for uploading a zip into a given directory
    """

    def __init__(self, conf, payload, files):
        sl = SendLog()
        sl.write(event="Uzu", action="init", userid=None)
        try:
            # root = conf.homeroot
            dyn_root = DynamicRoot(conf)
            payload = json.loads(payload)
            self.user = moodle2notouser(payload["user"])
            self.do_chmod = conf.chmod
            if self.user.errcode == 0:
                userloc = self.user.getNotoUser()
                destination = payload["destination"]
                # Get root variable ready
                root = dyn_root.getRoot(userloc)["root"]
                if destination == ".":
                    self.status = "Error : destination is not defined"
                    self.errcode = 500
                elif not os.path.exists(os.path.join(root, userloc)):
                    self.status = "Error : destination does not exist"
                    self.errcode = 440
                else:
                    self.blob = files["file"]  # payload['blob']
                    # userroot = os.path.join(root, userloc)
                    userroot = os.path.join(root, userloc)
                    self.access = {
                        "chmod": oct(os.stat(userroot).st_mode)[-3:],
                        "uid": os.stat(userroot).st_uid,
                        "gid": os.stat(userroot).st_gid,
                    }
                    self.root = os.path.join(userroot, destination)
                    self.basename = os.path.join(root)

                    self.status = "OK"
                    self.errcode = 0

            else:
                self.status = self.user.status
                self.errcode = self.user.errcode

        except Exception as e:
            self.status = "Error with payload: {0}".format(e)
            self.errcode = 500

    def _checkdest(self):
        root = self.root
        version = 1
        while os.path.exists(root):
            version += 1
            root = self.root + "-V" + str(version)

            if version > 100:  # avoid infinite loop
                self.status = "Error : cannot find a place to extract"
                self.errcode = -1
                return False
        self.root = root
        os.mkdir(self.root)
        return True

    def _postUzU(self):
        log = SendLog()
        if self._checkdest():
            self.status = "OK"
            self.errcode = 0
            zip = ZipBlob()

            try:
                zip.PutZip(self.blob, self.root)
            except Exception as e:
                if len(self.blob) == 0:
                    self.status = "Error: zip blob size is 0"
                else:
                    self.status = (
                        "Error: zip extract not working in this directory: {0}".format(
                            e
                        )
                    )
                self.errcode = -1
                log.write(
                    "Uzu FAILED", "from : " + self.root, self.user.getNotoUserid()
                )
                return []

            # apply file permission; skip on Windows
            if os.name != "nt":
                # safer to not use shell call
                for root, dirs, files in os.walk(self.root):
                    # Fails in Kubernetes, we're not root; there we have set uid/gid
                    # to the same values as used in  Jupyter notebook containers.
                    # TODO: do we need a configuration to trigger?
                    try:
                        for loc in files:
                            os.chown(
                                os.path.join(root, loc),
                                self.access["uid"],
                                self.access["gid"],
                            )
                    except PermissionError:
                        pass

                if self.do_chmod and "KUBERNETES_SERVICE_HOST" not in os.environ:
                    # chmod only performed if requested in configuration file.
                    # This chmod is not needed in Kubernetes.
                    os.system(
                        f"chown -R {self.access['uid']}:{self.access['gid']} '{self.root}'"
                    )
                    os.system(f"chmod -R {self.access['chmod']} {self.root}")

            log.write("Uzu SUCCESS", "from : " + self.root, self.user.getNotoUserid())
            return {"extractpath": self.root.replace(self.basename, "")}

        log.write("Uzu FAILED", "from : " + self.root, self.user.getNotoUserid())
        return []

    def GetPayload(self):
        return self._postUzU()

    def isok(self):

        if self.status == "OK":
            return True
        else:
            return False

    def GetStatus(self):
        status = {"code": self.errcode, "status": self.status}
        return status
