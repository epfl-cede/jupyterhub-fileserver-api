from tests.conftest import auth
import urllib.parse
import json
from tests.lib import request_items, calc_md5


def test_lof(client):
    req, md5, hmac = request_items('{{"user":{user_string},"path":"."}}')
    request = "/lof?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
        user=auth["user"],
        key=urllib.parse.quote(hmac),
        ts=req["timestamp"],
        payload=req["payload"],
        md5p=urllib.parse.quote(md5),
    )
    rv = client.get(request)
    data = json.loads(rv.data)
    payload = json.loads(data["payload"])
    md5_response = data["md5_payload"]
    md5_payload = calc_md5(data)

    # Test return code
    assert data["return"]["code"] == 0
    # Test if directory and files appear
    if payload[0]["name"] == "testdir":
        assert payload[0]["children"][0]["name"] == "testfile.txt"
        assert payload[1]["name"] == "aaa.txt"
    else:
        assert payload[1]["children"][0]["name"] == "testfile.txt"
        assert payload[0]["name"] == "aaa.txt"

    # Test md5 checksum
    assert md5_response == md5_payload
