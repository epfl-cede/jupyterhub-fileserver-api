from conftest import user_string, auth
from libs.fct_global import CalcMd5, CalcHmac
import datetime
import base64
import hashlib


def request_items(payload):
    payload = payload.format(user_string=user_string)
    req = {
        "payload": payload,
        "timestamp": str(int(datetime.datetime.now().timestamp())),
        "user": auth["user"],
    }
    md5 = CalcMd5(req).md5_payload()
    hmac = CalcHmac(req, auth["key"]).getHmac()

    return req, md5, hmac


def calc_md5(data):
    return base64.b64encode(
        hashlib.md5(data["payload"].encode("utf-8")).digest()
    ).decode("utf-8")
