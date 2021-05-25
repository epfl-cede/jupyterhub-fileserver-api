import json

from libs.fct_global import CalcMd5

from flask import jsonify


class Output:
    def __init__(self):
        self.status = None
        self.payload = None

    def SetStatus(self, status):
        self.status = status

    def SetPayload(self, payload):
        self.payload = json.dumps(payload)

    def generate(self):
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
        else:
            out = "Something is wrong here please contact support"

        return jsonify(out)
