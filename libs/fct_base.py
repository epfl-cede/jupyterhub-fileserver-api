import os
import json
from libs.fct_global import moodle2notouser, DynamicRoot


class RequestExecutor:
    """
    Base class for request execution functions
    """

    dyn_root = None
    user = None
    user_home_path = None
    userloc = None
    payload = None
    status = "OK"
    errcode = 0

    def __init__(self, conf, payload, log):
        # Determine root of user filesystem
        self.dyn_root = DynamicRoot(conf)
        if self.dyn_root.ndi is None and self.dyn_root.root is None:
            self.status = "Error: dynamic root not initialized"
            self.error = 500
            log.error("Dynamic root not initialized")
            return

        # Convert payload from request to JSON
        try:
            self.payload = json.loads(payload)
        except json.decoder.JSONDecodeError:
            self.status = "Error: can't convert payload to JSON"
            self.errcode = 500
            log.error("Payload conversion to JSON failed: {0}".format(payload))
            return

        # Evaluate current user
        self.user = moodle2notouser(self.payload["user"])
        if self.user.errcode != 0:
            self.status = "Error: couldn't determine user"
            self.errcode = 500
            log.error(
                "Couldn't determine user, error code: {0}".format(self.user.errcode)
            )
            return

        # Get user directory
        try:
            self.userloc = self.user.getNotoUser()
        except Exception as e:
            self.status = "Error: couldn't get Noto user: {0}".format(e)
            self.errcode = 500
            log.error("Couldn't get Noto user: {0}".format(e))
            return
        # Block empty user path
        if self.userloc == "":
            self.status = "Empty user home path rejected"
            self.errcode = 500
            self.root = self.dyn_root.get_invalid_path()
            return
        self.user_home_path = os.path.join(
            self.dyn_root.get_root(self.userloc)["root"], self.userloc
        )
        if not os.path.exists(self.user_home_path):
            self.status = "Error: user home does not exist"
            self.errcode = 500
            log.error("User home does not exist")
            return
        log.debug("User home is {0}".format(self.user_home_path))

    def is_ok(self):
        if self.status == "OK":
            return True
        else:
            return False

    def get_status(self):
        status = {"code": self.errcode, "status": self.status}
        return status
