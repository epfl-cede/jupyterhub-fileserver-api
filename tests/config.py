from app import app
import pytest
import os
import shutil


auth = {"user": "Szt7TQpqbCQHpCg0", "key": "pHV2QrraLMVPb6Ns"}

user_string = '{"id":"test2","primary_email":"test2@epfl.ch","auth_method":"test"}'


# Test setup
@pytest.fixture(scope="module")
def client():
    app.testing = True
    home = os.getenv("HOMEROOT")
    path = os.path.join(home, "test2")
    if not os.path.exists(path):
        os.mkdir(path)
        f = open(os.path.join(path, "aaa.txt"), "w")
    if not os.path.exists(os.path.join(path, "testdir")):
        os.mkdir(os.path.join(path, "testdir"))
        f = open(os.path.join(path, "testdir", "testfile.txt"), "w")
        f.close()
    with app.test_client() as client:
        yield client

    # Teardown
    shutil.rmtree(path, ignore_errors=True)
