import pytest
from app.repository import scapper_repository


@pytest.fixture
def mock_urls(monkeypatch):
    monkeypatch.setattr(scapper_repository.urls, "sessions", {
        "importacao": {
            "item": "opt_05",
            "sub": {
                "ImpVinhos": "subopt_01"
            }
        },
        "producao": {"item": "opt_02"}
    })
    monkeypatch.setattr(
        scapper_repository.urls,
        "get_url_scrapping",
        lambda ano, cod_opcao, cod_subopcao=None: (
            f"http://fakeurl/{ano}/{cod_opcao}/{cod_subopcao}"
        )
    )


def test_find_with_subitems_success(monkeypatch, mock_urls):
    monkeypatch.setattr(
        scapper_repository.reader,
        "read",
        lambda url: "<html><table class='tb_base tb_dados'></table></html>"
    )

    called = {}

    monkeypatch.setattr(
        "app.util.scrapping.strategy_with_subitems.WithSubItems.scrape",
        lambda self, html: called.setdefault(
            "scraped",
            {"data": "subitem ok"}
        )
    )

    result = scapper_repository.find_with_subitems(
        "2023", "importacao", "ImpVinhos"
    )

    assert result == {"data": "subitem ok"}
    assert "scraped" in called


def test_find_with_justitems_success(monkeypatch, mock_urls):
    monkeypatch.setattr(
        scapper_repository.reader,
        "read",
        lambda url: "<html><table class='tb_base tb_dados'></table></html>"
    )

    called = {}

    monkeypatch.setattr(
        "app.util.scrapping.strategy_just_item.JustItems.scrape",
        lambda self, html: called.setdefault(
            "scraped", {"data": "justitem ok"}
        )
    )

    result = scapper_repository.find_with_justitems("2023", "producao")

    assert result == {"data": "justitem ok"}
    assert "scraped" in called


def test_find_with_subitems_reader_fail(monkeypatch, mock_urls):
    monkeypatch.setattr(
        scapper_repository.reader,
        "read",
        lambda url: (_ for _ in ()).throw(Exception("Reader Error"))
    )

    result = scapper_repository.find_with_subitems(
        "2023", "importacao", "ImpVinhos"
    )

    assert result is None


def test_find_with_justitems_reader_fail(monkeypatch, mock_urls):
    monkeypatch.setattr(
        scapper_repository.reader,
        "read",
        lambda url: (_ for _ in ()).throw(Exception("Reader Error"))
    )

    result = scapper_repository.find_with_justitems("2023", "producao")

    assert result is None
