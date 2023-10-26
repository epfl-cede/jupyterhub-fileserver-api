import time
from libs.fct_global import CalcMd5, CalcHmac


class ValidateInput:
    def __init__(self, request, auth, ttl):
        self.request = request
        self.auth = auth
        self.ttl = ttl
        self.status = None
        self.errcode = None
        self.valid = None

    def validate(self):
        self.valid = False
        if self._validate_request():
            try:
                user = self.request["user"]
                timestamp = int(self.request["timestamp"])
                if self.auth.CheckUser(user):  # check that user exist
                    # check that timing is in the ttl range
                    if time.time() - timestamp <= self.ttl:
                        md5 = CalcMd5(request=self.request)
                        # check that payload has correct md5 (over payload) and hmac (includes secret)
                        if self.request["md5_payload"] == md5.md5_payload():
                            hmac = CalcHmac(
                                request=self.request, key=self.auth.UserKey(user)
                            )
                            # check key encryption
                            if self.request["key"] == hmac.getHmac():
                                self.status = "OK"
                                self.errcode = 0
                                return True
                            else:
                                self.status = "Error : checking hmac"
                                self.errcode = 104
                                return False
                        else:
                            self.status = "Error : checking md5 payload"
                            self.errcode = 103
                            return False
                    else:
                        self.status = (
                            "Error : checking timestamp increase ttl if persist"
                        )
                        self.errcode = 102
                        return False
                else:
                    self.status = "Error : authentication failed"
                    self.errcode = 401
                    return False
            except Exception as e:  # pragma: no cover
                self.status = "Error : treating the request: {}".format(e)
                self.errcode = -1
                return False
        else:
            self.status = (
                "Error : the request is not formatted correctly : " + self.status
            )
            self.errcode = 100
            return False

    def _validate_request(self):
        keys = ["user", "timestamp", "payload", "md5_payload", "key"]

        for key in keys:
            if key not in self.request:
                self.status = key + " is missing"
                return False
        return True

    def is_ok(self):

        if self.status == "OK":
            return True
        else:
            return False

    def get_status(self):
        status = {"code": self.errcode, "status": self.status}
        return status
