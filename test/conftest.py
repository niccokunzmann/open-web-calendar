import os
import sys
import pytest
from unittest.mock import Mock

HERE = os.path.dirname(__name__) or "."
sys.path.append(os.path.join(os.path.abspath(HERE), ".."))
sys.path.append(os.path.abspath(HERE))

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Prevent requests from sending out requests

    See https://docs.pytest.org/en/latest/monkeypatch.html#example-preventing-requests-from-remote-operations
    """
    monkeypatch.delattr("requests.sessions.Session.request")

@pytest.fixture()
def mock():
    return Mock()
