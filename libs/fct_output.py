import json
import logging

from libs.fct_global import CalcMd5

from flask import jsonify

log = logging.getLogger("output")


class Output:
    """
    Object keeping status and payload, and preparing response.
    """

    def __init__(self):
        self.status = None
        self.payload = None

    def set_status(self, status):
        self.status = status

    def set_payload(self, payload):
        self.payload = json.dumps(payload)

    def generate(self):
        """
        Generate response to HTTP request
        :return: JSON with payload, checksum and status
        """
        if self.status is not None:
            if self.payload is not None:
                request = {"payload": self.payload}
                md5 = CalcMd5(request)
                out = {
                    "return": self.status,
                    "payload": self.payload,
                    "md5_payload": md5.md5_payload(),
                }
            else:
                payload = "{}"
                request = {"payload": payload}
                md5 = CalcMd5(request)
                out = {
                    "return": self.status,
                    "payload": payload,
                    "md5_payload": md5.md5_payload(),
                }
            log.debug("Output generated: {0}".format(out))
        else:
            out = "Something is wrong here, please contact support"

        return jsonify(out)
