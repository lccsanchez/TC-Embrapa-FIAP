import pytest
from app.util import reader


def test_read_success(monkeypatch):
    class FakeResponse:
        text = "conteudo"
        encoding = "utf8"
        def raise_for_status(self): pass
    monkeypatch.setattr("requests.get", lambda url, timeout=10: FakeResponse())
    assert reader.read("http://fakeurl") == "conteudo"


def test_read_fail(monkeypatch):
    def fake_get(url, timeout=10):
        raise Exception("fail")
    monkeypatch.setattr("requests.get", fake_get)
    with pytest.raises(Exception):
        reader.read("http://failurl")


def test_read_timeout(monkeypatch):
    import requests

    def fake_get(url, timeout=10):
        raise requests.Timeout("timeout")
    monkeypatch.setattr("requests.get", fake_get)
    with pytest.raises(requests.Timeout):
        reader.read("http://timeout")
