from io import BytesIO
import zipfile
import os
import json
from werkzeug.utils import secure_filename
import base64

from libs.fct_global import moodle2notouser, SendLog


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
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    archivepath = filepath.replace(path, '')
                    zipf.write(filepath, archivepath)
        memory_file.seek(0)
        return base64.b64encode(memory_file.read()).decode("utf-8")

    def PutZip(self, blob, path):
        memory_file = BytesIO(blob.read())  # BytesIO(base64.b64decode(blob))
        with zipfile.ZipFile(memory_file, 'r') as zipf:
            os.chdir(path)
            zipf.extractall()


class ZfS:
    """
    This class is called for downloading a Zip from a given directory
    """

    def __init__(self, conf, payload, *kwargs):
        try:
            root = conf.homeroot
            payload = json.loads(payload)
            self.user = moodle2notouser(payload['user'])

            if self.user.errcode == 0:
                userloc = self.user.getNotoUser()
                folder = payload['folder']
                self.root = os.path.join(root, userloc, folder)
                self.origin = os.path.join(userloc, folder)
                if not os.path.exists(self.root):
                    self.status = "Error : destination does not exist"
                    self.errcode = 440
                else:
                    self.status = "OK"
                    self.errcode = 0
            else:
                self.status = self.user.status
                self.errcode = self.user.errcode

        except:
            self.status = "Error with payload"
            self.errcode = 500

    def _getZfS(self):
        log = SendLog()
        try:
            self.status = "OK"
            self.errcode = 0
            zip = ZipBlob()
            blob = zip.GetZip(self.root)
            log.write("Zfs SUCCESS", "from : " + self.root, self.user.getNotoUserid())
            return {'origin': self.origin, 'blob': blob, "method": "base64", "mime": "application/zip"}
        except:
            self.status = "Error : zip is not working in this directory"
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
        status = {
            'code': self.errcode,
            'status': self.status
        }
        return status


class UzU:
    """
    This class is called for uploading a zip into a given directory
    """

    def __init__(self, conf, payload, files):
        try:
            root = conf.homeroot
            payload = json.loads(payload)
            self.user = moodle2notouser(payload['user'])
            if self.user.errcode == 0:
                userloc = self.user.getNotoUser()
                destination = payload['destination']
                if destination == ".":
                    self.status = "Error : destination is not defined"
                    self.errcode = 500
                elif not os.path.exists(os.path.join(root, userloc)):
                    self.status = "Error : destination does not exist"
                    self.errcode = 440
                else:
                    self.blob = files['file']  # payload['blob']
                    print("blob", self.blob)
                    self.root = os.path.join(root, userloc, destination)
                    self.basename = os.path.join(root)

                    self.status = "OK"
                    self.errcode = 0

            else:
                self.status = self.user.status
                self.errcode = self.user.errcode

        except:
            self.status = "Error with payload"
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
        try:
            if self._checkdest():
                self.status = "OK"
                self.errcode = 0
                zip = ZipBlob()
                zip.PutZip(self.blob, self.root)
                log.write("Uzu SUCCESS", "from : " + self.root, self.user.getNotoUserid())
            return {'extractpath': self.root.replace(self.basename, '')}
        except:
            self.status = "Error : zip extract not working in this directory"
            self.errcode = -1
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
        status = {
            'code': self.errcode,
            'status': self.status
        }
        return status
