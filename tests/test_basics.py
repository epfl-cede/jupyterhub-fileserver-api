import json


def test_root(client):
    """
    Always returns the same content
    """
    rv = client.get("/")
    data = json.loads(rv.data)

    assert rv.status == "200 OK"
    assert data["return"]["code"] == 0
    assert data["md5_payload"] == "mZFLkyvTelC5g8XnyQrpOw=="


def test_healthz(client):
    """
    Liveliness check for Kubernetes
    """
    rv = client.get("/healthz")

    assert rv.status == "200 OK"
