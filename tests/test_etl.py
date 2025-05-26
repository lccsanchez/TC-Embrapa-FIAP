from app.util import etl


def test_execute_returns_none_on_empty():
    result = etl.execute({"key": None})
    assert result is None


def test_execute_returns_none_on_empty_dataframe(monkeypatch):
    monkeypatch.setattr(etl, "_load", lambda url, key=None: None)
    result = etl.execute({"key": "url"})
    assert result is None


def test_execute_success(monkeypatch):
    class FakeDF:
        empty = False

    monkeypatch.setattr(etl, "_load", lambda url, key=None: FakeDF())
    result = etl.execute({"key": "url"})
    assert isinstance(result, list)
    assert result[0][0] == "key"


def test_execute_load_raises(monkeypatch):
    def raise_exception(url, key=None):
        raise Exception("fail")

    monkeypatch.setattr(etl, "_load", raise_exception)
    result = etl.execute({"key": "url"})
    assert result is None
