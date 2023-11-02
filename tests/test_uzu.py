import os
from tests.conftest import auth
import urllib.parse
import json
from tests.lib import request_items, calc_md5


def test_uzu(client):
    req, md5, hmac = request_items('{{"user":{user_string},"destination":"zipdir"}}')
    zip_file = open("tests/application-1.zip", "rb")
    data = {"file": (zip_file, "test.zip")}
    request = "/uzu?user={user}&timestamp={ts}&payload={payload}&md5_payload={md5p}&key={key}".format(
        user=auth["user"],
        key=urllib.parse.quote(hmac),
        ts=req["timestamp"],
        payload=req["payload"],
        md5p=urllib.parse.quote(md5),
    )

    rv = client.post(request, data=data, content_type="multipart/form-data")

    data = json.loads(rv.data)
    md5_response = data["md5_payload"]
    md5_payload = calc_md5(data)
    file_list = os.listdir(os.path.join(os.getenv("HOMEROOT"), "test2", "zipdir"))

    # Test return code
    assert data["return"]["code"] == 0
    # Test md5 checksum
    assert md5_response == md5_payload
    # Test if file has been created
    assert file_list[0] == "part1.txt"
