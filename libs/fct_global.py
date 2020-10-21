import hashlib

class CalcMd5:
    """
    This class is used for calculating md5 values for payload and key verification
    """

    def __init__(self, request, key=None):
        """
        Initiate the CalcMd5 class
        :param request: dict with request arguments
        :param key: secret key for this user
        """

        self.payload = request['payload']
        self.OnlyPayload = True
        if key is not None:  # if key is not defined only payload can be calculated
            self.user = request['user']
            self.key = key
            self.timestamp = request['timestamp']
            self.OnlyPayload = False

        self.save_md5 = None
        self.save_md5_payload = None

    def md5_payload(self):
        self.save_md5_payload = str(hashlib.md5(self.payload.encode('utf-8')).hexdigest())
        return self.save_md5_payload

    def md5(self):
        if not self.OnlyPayload:
            if self.save_md5_payload is None:
                self.md5_payload()
            string = self.user + self.timestamp  + self.save_md5_payload + self.key
            self.save_md5 = str(hashlib.md5(string.encode('utf-8')).hexdigest())
        return self.save_md5
