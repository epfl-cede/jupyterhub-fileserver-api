from io import BytesIO
import zipfile
import os
import base64
import logging

from libs.fct_global import SendLog
from libs.fct_base import RequestExecutor

log = logging.getLogger("zfs")


class ZipBlob:
    """
    Manage zip file from and to blob base64
    """

    def get_zip(self, path):
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
        zipf.close()
        return base64.b64encode(memory_file.read()).decode("utf-8")

    def put_zip(self, blob, path):
        """
        Extract data received as ZIP archive
        :param blob: byte array
        :param path: output file path
        """
        memory_file = BytesIO(blob.read())  # BytesIO(base64.b64decode(blob))
        with zipfile.ZipFile(memory_file, "r") as zipf:
            os.chdir(path)
            zipf.extractall()
        # Get rid of file handles
        os.chdir("..")
        zipf.close()


class Zipper(RequestExecutor):
    """
    Abstract class for requests dealing with ZIP files.
    """

    def handle_archive(self):
        raise NotImplementedError

    def get_payload(self):
        return self.handle_archive()


class ZfS(Zipper):
    """
    This class is called for downloading a Zip from a given directory
    """

    def __init__(self, conf, payload, *kwargs):
        sl = SendLog()
        sl.write(event="ZfS", action="init", userid=None)
        log.debug("ZfS init")

        RequestExecutor.__init__(self, conf, payload, log)
        # Any exception during base class init?
        if self.errcode != 0:
            return

        try:
            folder = self.payload["folder"]
        except KeyError:
            self.status = "Item 'folder' not found in payload"
            self.errcode = 500
            log.error("Item 'folder' not found in payload")
            return

        self.root = os.path.join(self.user_home_path, folder)
        self.origin = os.path.join(self.userloc, folder)
        sl.write(event="self.root", action=self.root, userid=None)
        log.debug("ZIP source path: {0}".format(self.origin))
        if not os.path.exists(self.root):
            self.status = "Error: source '{0}' does not exist".format(self.root)
            self.errcode = 500
            log.error("ZIP source does not exist: {0}".format(self.root))
        else:
            self.status = "OK"
            self.errcode = 0

        log.debug("ZfS init complete")

    def handle_archive(self):
        """
        Pack a directory into a ZIP file.
        :return: dict for response payload
        """
        log.debug("ZfS handle_archive start")
        sl = SendLog()
        try:
            self.status = "OK"
            self.errcode = 0
            zip = ZipBlob()
            blob = zip.get_zip(self.root)
            sl.write("Zfs SUCCESS", "from : " + self.root, self.user.getNotoUserid())
            log.debug("ZfS handle_archive completed")
            return {
                "origin": self.origin,
                "blob": blob,
                "method": "base64",
                "mime": "application/zip",
            }
        except Exception as e:
            self.status = "Error: zip is not working in this directory: {0}".format(e)
            self.errcode = 500
            sl.write("Zfs FAILED", "from : " + self.root, self.user.getNotoUserid())
            log.error("Error: zip is not working in this directory: {0}".format(e))
            return []


class UzU(Zipper):
    """
    This class is called for uploading a zip into a given directory
    """

    def __init__(self, conf, payload, files):
        sl = SendLog()
        sl.write(event="Uzu", action="init", userid=None)
        log.debug("UzU init")

        RequestExecutor.__init__(self, conf, payload, log)
        # Any exception during base class init?
        if self.errcode != 0:
            return

        self.do_chmod = conf.chmod

        try:
            destination = self.payload["destination"]
        except KeyError:
            self.status = "Item 'destination' not found in payload"
            self.errcode = 500
            log.error("Item 'destination' not found in payload")
            return

        log.debug("Destination is {0}".format(destination))

        if destination == ".":
            self.status = "Error: destination is not defined"
            self.errcode = 500
            log.error("ZIP destination is not defined")
            return
        else:
            try:
                self.blob = files["file"]  # payload['blob']
            except KeyError:
                self.status = "No upload archive found in request"
                self.errcode = 500
                log.error(self.status)
                return
            log.debug("Blob is {0}".format(self.blob))
            self.access = {
                "chmod": oct(os.stat(self.user_home_path).st_mode)[-3:],
                "uid": os.stat(self.user_home_path).st_uid,
                "gid": os.stat(self.user_home_path).st_gid,
            }
            self.root = os.path.join(self.user_home_path, destination)
            self.basename = os.path.join(self.root)

            self.status = "OK"
            self.errcode = 0

            log.debug("UzU init complete")
            return

    def _checkdest(self):
        """
        Test if destination directory already exists. Add/Increase version suffix if needed.
        :return: False, if versions exceed limit.
        """
        root = self.root
        version = 1
        while os.path.exists(root):
            version += 1
            root = self.root + "-V" + str(version)

            if version > 100:  # avoid infinite loop
                self.status = "Error : ZIP destination folder version limit reached"
                self.errcode = 500
                log.debug("ZIP destination folder version limit reached")
                return False
        self.root = root
        os.mkdir(self.root)
        return True

    def handle_archive(self):
        """
        Unpack byte array received in payload as a ZIP file.
        """
        log.debug("UzU handle_archive start")
        sl = SendLog()
        if self._checkdest():
            self.status = "OK"
            self.errcode = 0
            zip = ZipBlob()

            log.debug("Extract archive")
            try:
                zip.put_zip(self.blob, self.root)
            except Exception as e:
                self.status = (
                    "Error: zip extract not working in this directory: {0}".format(e)
                )
                self.errcode = -1
                sl.write("Uzu FAILED", "from : " + self.root, self.user.getNotoUserid())
                log.error(
                    "Error: zip extract not working in this directory: {0}".format(e)
                )
                return []

            log.debug("Archive extracted, fixing permissions")
            # apply file permission; skip on Windows
            if os.name != "nt":
                # safer to not use shell call
                for root, dirs, files in os.walk(self.root):
                    # Fails in Kubernetes, we're not root; there we have set uid/gid
                    # to the same values as used in  Jupyter notebook containers.
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

            sl.write("Uzu SUCCESS", "from : " + self.root, self.user.getNotoUserid())

            log.debug("UzU handle_archive completed")
            return {"extractpath": os.path.relpath(self.root, self.user_home_path)}

        sl.write("Uzu FAILED", "from : " + self.root, self.user.getNotoUserid())
        return []
