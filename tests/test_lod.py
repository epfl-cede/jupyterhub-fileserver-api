from tests.conftest import auth
import urllib.parse
import json
from tests.lib import request_items, calc_md5


def test_lod(client):
    req, md5, hmac = request_items('{{"user":{user_string},"path":"."}}')
    request = "/lod?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
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
    # Test if directory appears
    assert payload["children"][0]["name"] == "testdir"
    # Test md5 checksum
    assert md5_response == md5_payload
