import pytest
from fastapi import HTTPException

from app.service import imp_exp_service


def test_get_tipo_registro():
    assert (
        imp_exp_service._get_tipo_registro("importacao").__name__
        == "RegistroImportacao"
    )
    assert (
        imp_exp_service._get_tipo_registro("exportacao").__name__
        == "RegistroExportacao"
    )


def test_get_tipo_url():
    urls = imp_exp_service._get_tipo_url("importacao")
    assert "ImpVinhos" in urls

    urls = imp_exp_service._get_tipo_url("exportacao")
    assert "ExpVinho" in urls


def test_find_uses_scrapper(monkeypatch):
    monkeypatch.setattr(
        imp_exp_service.scapper_repository,
        "find_with_justitems",
        lambda *args, **kwargs: {"scrapper": "data"},
    )
    monkeypatch.setattr(
        imp_exp_service.imp_exp_db_repository,
        "find",
        lambda *args, **kwargs: {"should_not": "be_used"},
    )

    result = imp_exp_service.find("2023", "importacao", "importacao")
    assert result == {"scrapper": "data"}


def test_find_fallback_to_db(monkeypatch):
    monkeypatch.setattr(
        imp_exp_service.scapper_repository,
        "find_with_justitems",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        imp_exp_service.imp_exp_db_repository,
        "find",
        lambda *args, **kwargs: {"db": "data"},
    )

    result = imp_exp_service.find("2023", "importacao", "importacao")
    assert result == {"db": "data"}


def test_find_not_found(monkeypatch):
    monkeypatch.setattr(
        imp_exp_service.scapper_repository,
        "find_with_justitems",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        imp_exp_service.imp_exp_db_repository, "find", lambda *args, **kwargs: None
    )

    with pytest.raises(HTTPException) as excinfo:
        imp_exp_service.find("2023", "importacao", "importacao")

    assert excinfo.value.status_code == 404


def test_save_all_success(monkeypatch):
    monkeypatch.setattr(
        imp_exp_service.imp_exp_embrapa_repository,
        "find_all",
        lambda *args, **kwargs: ["item1", "item2"],
    )

    called = {}

    def fake_add_all(tipo, data):
        called["tipo"] = tipo
        called["data"] = data

    monkeypatch.setattr(imp_exp_service.imp_exp_db_repository, "add_all", fake_add_all)

    imp_exp_service.save_all("importacao")

    assert called["tipo"] == "importacao"
    assert called["data"] == ["item1", "item2"]


def test_save_all_etl_fails(monkeypatch):
    monkeypatch.setattr(
        imp_exp_service.imp_exp_embrapa_repository,
        "find_all",
        lambda *args, **kwargs: None,
    )

    called = {}

    def fake_add_all(tipo, data):
        called["tipo"] = tipo
        called["data"] = data

    monkeypatch.setattr(imp_exp_service.imp_exp_db_repository, "add_all", fake_add_all)

    imp_exp_service.save_all("importacao")

    assert called["tipo"] == "importacao"
    assert called["data"] is None
