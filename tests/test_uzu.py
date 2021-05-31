import os

from tests.conftest import auth, user_string
import datetime
import urllib.parse
import json
import hashlib
import base64
from libs.fct_global import CalcMd5, CalcHmac


def test_root(client):
    rv = client.get("/")
    data = json.loads(rv.data)

    assert rv.status == "200 OK"
    assert data["return"]["code"] == 0
    assert data["md5_payload"] == "mZFLkyvTelC5g8XnyQrpOw=="


def test_uzu(client):
    payload = '{{"user":{user_string},"destination":"zipdir"}}'.format(
        user_string=user_string
    )
    req = {
        "payload": payload,
        "timestamp": str(int(datetime.datetime.now().timestamp())),
        "user": auth["user"],
    }
    zip_file = open("tests/application-1.zip", "rb")
    data = {"file": (zip_file, "test.zip")}

    md5 = CalcMd5(req).md5_payload()
    hmac = CalcHmac(req, auth["key"]).getHmac()
    request = "/uzu?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
        user=auth["user"],
        key=urllib.parse.quote(hmac),
        ts=req["timestamp"],
        payload=req["payload"],
        md5p=urllib.parse.quote(md5),
    )

    rv = client.post(request, data=data, content_type="multipart/form-data")

    data = json.loads(rv.data)
    payload = json.loads(data["payload"])
    md5_response = data["md5_payload"]
    md5_payload = base64.b64encode(
        hashlib.md5(data["payload"].encode("utf-8")).digest()
    ).decode("utf-8")
    file_list = os.listdir(os.path.join(os.getenv("HOMEROOT"), "test2", "zipdir"))

    # Test return code
    assert data["return"]["code"] == 0
    # Test md5 checksum
    assert md5_response == md5_payload
    # Test if file has been created
    assert file_list[0] == "part1.txt"
