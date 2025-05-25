from app.service import op_internas_service


def test_get_tipo_registro():
    assert (
        op_internas_service._get_tipo_registro("producao").__name__
        == "RegistroProducao"
    )
    assert (
        op_internas_service._get_tipo_registro(
            "comercio"
        ).__name__
        == "RegistroComercio"
    )
    assert (
        op_internas_service._get_tipo_registro("processamento").__name__
        == "RegistroProcessamento"
    )


def test_get_tipo_url():
    urls = op_internas_service._get_tipo_url("producao")
    assert any("producao" in str(url).lower() for url in urls.values())

    urls = op_internas_service._get_tipo_url("comercio")
    assert (
        any(
            "comercio" in str(url).lower() or
            "comercializacao" in str(url).lower()
            for url in urls.values()
        )
        or
        any(
            "comercio" in str(key).lower() or
            "comercializacao" in str(key).lower()
            for key in urls.keys()
        )
    )

    urls = op_internas_service._get_tipo_url("processamento")
    assert any("processa" in str(url).lower() for url in urls.values())


def test_find_uses_scrapper(monkeypatch):
    monkeypatch.setattr(
        "app.repository.scapper_repository.find_with_subitems",
        lambda *args, **kwargs: {"scrapper": "data"}
    )
    result = op_internas_service.find(2023, "producao", "sub")
    assert result == {"scrapper": "data"}


def test_find_fallback_to_db(monkeypatch):
    monkeypatch.setattr(
        "app.repository.scapper_repository.find_with_subitems",
        lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        "app.service.op_internas_service._get_tipo_registro",
        lambda *args, **kwargs: "tipo_registro_mock"
    )
    monkeypatch.setattr(
        "app.repository.op_internas_db_repository.find",
        lambda *args, **kwargs: {"db": "data"}
    )

    result = op_internas_service.find(2023, "producao", "sub")
    assert result == {"db": "data"}


def test_save_all_success(monkeypatch):
    monkeypatch.setattr(
        "app.service.op_internas_service._get_tipo_registro",
        lambda *args, **kwargs: "tipo_registro_mock"
    )
    monkeypatch.setattr(
        "app.service.op_internas_service._get_tipo_url",
        lambda *args, **kwargs: "url_mock"
    )
    monkeypatch.setattr(
        "app.repository.op_internas_embrapa_repository.find_all",
        lambda *args, **kwargs: ["item1", "item2"]
    )

    called = {}

    def fake_add_all(nome, items):
        called["nome"] = nome
        called["items"] = items

    monkeypatch.setattr(
        "app.repository.op_internas_db_repository.add_all",
        fake_add_all
    )

    op_internas_service.save_all("producao")

    assert called["nome"] == "producao"
    assert called["items"] == ["item1", "item2"]


def test_save_all_etl_fails(monkeypatch):
    monkeypatch.setattr(
        "app.service.op_internas_service._get_tipo_registro",
        lambda *args, **kwargs: "tipo_registro_mock"
    )
    monkeypatch.setattr(
        "app.service.op_internas_service._get_tipo_url",
        lambda *args, **kwargs: "url_mock"
    )
    monkeypatch.setattr(
        "app.repository.op_internas_embrapa_repository.find_all",
        lambda *args, **kwargs: None
    )

    called = {}

    def fake_add_all(nome, items):
        called["nome"] = nome
        called["items"] = items

    monkeypatch.setattr(
        "app.repository.op_internas_db_repository.add_all",
        fake_add_all
    )

    op_internas_service.save_all("producao")

    assert called["nome"] == "producao"
    assert called["items"] is None
