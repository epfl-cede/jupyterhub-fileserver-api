from tests.conftest import auth
import urllib.parse
import json
from tests.lib import request_items

"""
Test various error code with manipulated request values
"""


def test_hmac(client):
    req, md5, hmac = request_items('{{"user":{user_string},"path":"."}}')
    hmac = "0000000"
    request = "/ls?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
        user=auth["user"],
        key=urllib.parse.quote(hmac),
        ts=req["timestamp"],
        payload=req["payload"],
        md5p=urllib.parse.quote(md5),
    )
    rv = client.get(request)
    data = json.loads(rv.data)
    assert data["return"]["code"] == 104


def test_md5(client):
    req, md5, hmac = request_items('{{"user":{user_string},"path":"."}}')
    md5 = "0000000"
    request = "/ls?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
        user=auth["user"],
        key=urllib.parse.quote(hmac),
        ts=req["timestamp"],
        payload=req["payload"],
        md5p=urllib.parse.quote(md5),
    )
    rv = client.get(request)
    data = json.loads(rv.data)
    assert data["return"]["code"] == 103


def test_ttl(client):
    req, md5, hmac = request_items('{{"user":{user_string},"path":"."}}')
    request = "/ls?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
        user=auth["user"],
        key=urllib.parse.quote(hmac),
        ts=10,
        payload=req["payload"],
        md5p=urllib.parse.quote(md5),
    )
    rv = client.get(request)
    data = json.loads(rv.data)
    assert data["return"]["code"] == 102


def test_auth_user(client):
    req, md5, hmac = request_items('{{"user":{user_string},"path":"."}}')
    auth = {"user": "aaaaaaaa", "key": "11111111"}
    request = "/ls?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
        user=auth["user"],
        key=urllib.parse.quote(hmac),
        ts=req["timestamp"],
        payload=req["payload"],
        md5p=urllib.parse.quote(md5),
    )
    rv = client.get(request)
    data = json.loads(rv.data)
    assert data["return"]["code"] == 401


def test_missing_param(client):
    req, md5, hmac = request_items('{{"user":{user_string},"path":"."}}')
    auth = {"user": "00000000", "key": "aaaaaaaa"}
    request = (
        "/ls?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}".format(
            user=auth["user"],
            ts=req["timestamp"],
            payload=req["payload"],
            md5p=urllib.parse.quote(md5),
        )
    )
    rv = client.get(request)
    data = json.loads(rv.data)
    assert data["return"]["code"] == 100
