from tests.conftest import auth
import urllib.parse
import json
import base64
import zipfile
from io import BytesIO
from tests.lib import request_items, calc_md5


def test_zfs(client):
    req, md5, hmac = request_items('{{"user":{user_string},"folder":"testdir"}}')
    request = "/zfs?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
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
    zip_file = zipfile.ZipFile(BytesIO(base64.b64decode(payload["blob"])))

    # Test return code
    assert data["return"]["code"] == 0
    # Test md5 checksum
    assert md5_response == md5_payload
    # Test if ZIP contains desired file
    assert zip_file.namelist()[0] == "testfile.txt"
