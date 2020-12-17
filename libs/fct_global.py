import base64
import hashlib, hmac

import json
from notouser import notoUser
from cedelogger import cedeLogger
import logging


class CalcHmac:
    """
    This class is used to calculate the HMAC-SHA256 key for authentication
    """

    def __init__(self, request, key):
        """
        Initiate the CalcHmac class
        :param request: dict with request arguments
        :param key: secret key for this user
        """

        self.payload = request['payload']
        self.user = request['user']
        self.key = key
        self.timestamp = request['timestamp']
        self.md5_payload = base64.b64encode(hashlib.md5(self.payload.encode('utf-8')).digest()).decode('utf-8')
        self.hmac = None

    def getHmac(self):
        """
        This function calculate the hmac sha256 using the key
        :return: the base64 hmac of self.user + self.timestamp + self.save_md5_payload
        """

        string = self.user + self.timestamp + self.md5_payload
        self.hmac = base64.b64encode(
            hmac.new(self.key.encode('utf-8'), string.encode('utf-8'), digestmod=hashlib.sha256).digest())

        return self.hmac.decode('utf-8')


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

    def md5_payload(self):
        """
        Calculate the md5 of the payload
        :return: base64 md5(payload)
        """
        self.md5_payload = base64.b64encode(hashlib.md5(self.payload.encode('utf-8')).digest())
        return self.md5_payload.decode('utf-8')


class moodle2notouser:
    """
    This class is used to do operation on login info from moodle into noto
    """

    def __init__(self, userpayload):
        try:
            self.id = userpayload['id']
            self.email = userpayload['primary_email']
            self.auth_meth = userpayload['auth_method']
        except:
            self.status = "Error with user payload"
            self.errcode = 510
        n = notoUser()
        try:
            self.NotoUser = n.userFromAPI(self.id, self.email)
            print("USER" , self.NotoUser)
            self.status = "OK"
            self.errcode = 0
        except:
            self.status = "Error with notoUser"
            self.errcode = 515

    def getNotoUser(self):
        return self.NotoUser['normalised']

    def getNotoUserid(self):
        return self.NotoUser['uid']


class SendLog:
    """
    This class is used to send log to noto syslog
    """

    def __init__(self):
        self.logger = cedeLogger(tag='fsapi')

    def write(self, event, action, userid):
        self.logger.log({'event': event, 'action': action, 'uid': userid}, level=logging.CRITICAL)
