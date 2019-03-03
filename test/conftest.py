import os
import sys
import pytest
from unittest.mock import Mock
import requests

HERE = os.path.dirname(__name__) or "."
sys.path.append(os.path.join(os.path.abspath(HERE), ".."))
sys.path.append(os.path.abspath(HERE))

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Prevent requests from sending out requests

    See https://docs.pytest.org/en/latest/monkeypatch.html#example-preventing-requests-from-remote-operations
    """
    def test_cannot_call_outside(*args, **kw):
        raise RuntimeError("Tests are not allowed to make requests to the"
                           " Internet. You can use cache_url() to mock that.")
    monkeypatch.setattr(requests.sessions.Session, "request", test_cannot_call_outside)

@pytest.fixture()
def mock():
    return Mock()
