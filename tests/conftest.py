from app import app
import pytest
import os
import shutil


auth = {"user": "00000000", "key": "11111111"}

user_id = "test2@epfl.ch"
user_string = '{"id":' + user_id + ',"primary_email":' + user_id + ',"auth_method":"test"}'


# Test setup
@pytest.fixture(scope="module")
def client():
    """
    Setup of test client and test files
    """
    app.testing = True
    home = os.getenv("HOMEROOT")
    path = os.path.join(home, user_id)
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
