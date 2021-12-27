
import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import init_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    print("In File: test_flaskr.py, Line: 14",db_fd,db_path)
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_empty_db(client):
    """Start with a blank database."""
    print("In File: test_flaskr.py, Line: 28",client)
    rv = client.get('/')
    # assert b'No entries here so far' in rv.data


def login(client, username, password):
    print("In File: test_flaskr.py, Line: 34","username")
    assert username == password
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def test_login_logout(client):
    """Make sure login and logout works."""
    rv =   login(client,"khuong","123")
    assert b'You were logged in' in rv.data