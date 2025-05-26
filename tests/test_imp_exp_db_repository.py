from unittest.mock import MagicMock

import pytest
from sqlalchemy import literal_column, select

from app.repository import imp_exp_db_repository


class FakeSubquery:
    def select(self):
        return select(literal_column("1")).subquery()

    def __clause_element__(self):
        return select(literal_column("1")).subquery()


@pytest.fixture
def mock_session(monkeypatch):
    session = MagicMock()
    session.rollback = MagicMock()
    context_manager = MagicMock()
    context_manager.__enter__.return_value = session
    context_manager.__exit__.return_value = None

    monkeypatch.setattr(imp_exp_db_repository, "SessionLocal", lambda: context_manager)

    return session


def test_add_all_success(monkeypatch, mock_session):
    monkeypatch.setattr(
        imp_exp_db_repository, "remove_all", lambda nome, session=None: None
    )

    imp_exp_db_repository.add_all("importacao", ["item1", "item2"])

    mock_session.add_all.assert_called_once_with(["item1", "item2"])
    mock_session.commit.assert_called_once()


def test_add_all_exception(monkeypatch, mock_session):
    monkeypatch.setattr(
        imp_exp_db_repository, "remove_all", lambda nome, session=None: None
    )

    mock_session.add_all.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        imp_exp_db_repository.add_all("importacao", ["item1"])


def test_remove_all_success(mock_session):
    query = mock_session.query.return_value
    filt2 = query.filter.return_value

    filt2.delete.return_value = 1

    imp_exp_db_repository.remove_all("importacao", session=mock_session)

    assert query.join.called
    assert query.filter.called
    assert filt2.delete.called


def test_remove_all_exception(monkeypatch, mock_session):
    query = mock_session.query.return_value
    filt2 = query.filter.return_value

    filt2.delete.side_effect = Exception("Delete error")

    with pytest.raises(Exception, match="Delete error"):
        imp_exp_db_repository.remove_all("importacao", session=mock_session)


def test_find_success(monkeypatch, mock_session):
    monkeypatch.setattr("app.util.converter.imp_exp_to_dto", lambda x: ["converted"])

    query = mock_session.query.return_value
    join2 = query.join.return_value
    filt2 = join2.filter.return_value
    opts = filt2.options.return_value
    ordered = opts.order_by.return_value

    ordered.all.return_value = ["fake_result"]

    result = imp_exp_db_repository.find(2023, "importacao", "importacao")

    assert result == ["converted"]
