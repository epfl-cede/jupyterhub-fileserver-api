import time

from libs.fct_global import CalcMd5


class ValidateInput():
    def __init__(self, request, auth, ttl, loc):
        self.request = request
        self.auth = auth
        self.ttl = ttl
        self.loc = loc.keys()
        self.status = None
        self.errcode = None
        self.valid = None

    def validate(self):
        self.valid = False
        if self._validate_request():
            try:
                user = self.request['user']
                timestamp = int(self.request['timestamp'])
                if self.auth.CheckUser(user):  # check that user exist
                    if time.time() - timestamp <= self.ttl:  # check that timing is in the ttl range
                        md5 = CalcMd5(request=self.request, key=self.auth.UserKey(user))
                        if self.request['md5_payload'] == md5.md5_payload():  # check that payload has correct md5
                            if self.request['md5'] == md5.md5():  # check key encryption
                                if self.request['command'] in self.loc:
                                    self.status = "OK"
                                    self.errcode = 0
                                    return True
                                else:
                                    self.status = "Error : Command unknown"
                                    self.errcode = 105
                                    return False
                            else:
                                self.status = "Error : checking md5"
                                self.errcode = 104
                                return False
                        else:
                            self.status = "Error : checking md5 payload"
                            self.errcode = 103
                            return False
                    else:
                        self.status = "Error : checking timestamp increase ttl if persist"
                        self.errcode = 102
                        return False
                else:
                    self.status = "Error : user is unknown"
                    self.errcode = 101
                    return False
            except:
                self.status = "Error : treating the request"
                self.errcode = -1
                return False
        else:
            self.status = "Error : the request is not formatted correctly : " + self.status
            self.errcode = 100
            return False

    def _validate_request(self):
        keys = ['user', 'timestamp', 'command', 'payload', 'md5_payload', 'md5']

        for key in keys:
            if key not in self.request:
                self.status = key + " is missing"
                return False
        return True

    def isok(self):

        if self.status == "OK":
            return True
        else:
            return False
    def GetStatus(self):
        status = {
            'code' : self.errcode,
            'status' : self.status
        }
        return status
