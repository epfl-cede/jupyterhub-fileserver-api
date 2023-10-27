import json


def test_stats(client):
    rv = client.get("/stats")
    data = json.loads(rv.data)

    assert rv.status == "200 OK"
    assert data["config"]["APPLICATION_ROOT"] != ""


def test_endpoint_stats(client):
    rv = client.get("/endpoints_stats")
    data = json.loads(rv.data)

    assert rv.status == "200 OK"
    assert len(data["duration"]) > 0
