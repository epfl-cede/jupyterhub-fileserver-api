from io import BytesIO
import zipfile
import os
import json
from werkzeug.utils import secure_filename
import base64


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
        memory_file = BytesIO(base64.b64decode(blob))
        with zipfile.ZipFile(memory_file, 'r') as zipf:
            os.chdir(path)
            zipf.extractall()


class ZfS:
    def __init__(self, conf, payload):
        try:
            root = conf.homeroot
            payload = json.loads(payload)
            userloc = secure_filename(payload['user'])
            folder = secure_filename(payload['folder'])
            self.root = os.path.join(root, userloc, folder)
            self.origin = os.path.join(userloc, folder)
            self.status = "OK"
            self.errcode = 0

        except:
            self.status = "Error with payload"
            self.errcode = 500

    def _getZfS(self):
        try:
            self.status = "OK"
            self.errcode = 0
            zip = ZipBlob()
            blob = zip.GetZip(self.root)
            return {'origin': self.origin, 'blob': blob, "method": "base64", "mime": "application/zip"}
        except:
            self.status = "Error : zip is not working in this directory"
            self.errcode = -1
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
    def __init__(self, conf, payload):
        try:
            root = conf.homeroot
            payload = json.loads(payload)
            userloc = secure_filename(payload['user'])
            destination = secure_filename(payload['destination'])
            if destination == ".":
                self.status = "Error : destination is not defined"
                self.errcode = 500
            else:
                self.blob = payload['blob']
                self.root = os.path.join(root, userloc, destination)
                self.basename = os.path.join(root)

                self.status = "OK"
                self.errcode = 0

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

    def _putUzU(self):
        try:
            if self._checkdest():
                self.status = "OK"
                self.errcode = 0
                zip = ZipBlob()
                zip.PutZip(self.blob, self.root)
            return {'extractpath': self.root.replace(self.basename, '')}
        except:
            self.status = "Error : zip extract not working in this directory"
            self.errcode = -1
            return []

    def GetPayload(self):
        return self._putUzU()

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
