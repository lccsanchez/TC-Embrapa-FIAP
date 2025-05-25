import pytest
from unittest.mock import MagicMock
from app.repository import op_internas_db_repository
from sqlalchemy import select, literal_column


class FakeSubquery:
    def select(self):
        return select(literal_column("1")).subquery()

    def __clause_element__(self):
        return select(literal_column("1")).subquery()


@pytest.fixture
def mock_session(monkeypatch):
    session = MagicMock()
    monkeypatch.setattr(op_internas_db_repository, "SessionLocal", lambda: session)
    return session


def test_find_success(monkeypatch, mock_session):
    monkeypatch.setattr("app.util.converter.model_to_dto", lambda x: ["converted"])

    query = mock_session.query.return_value
    join2 = query.join.return_value
    filt2 = join2.filter.return_value
    opts = filt2.options.return_value
    ordered = opts.order_by.return_value

    ordered.all.return_value = ["fake_result"]

    from app.model.model import RegistroProducao

    result = op_internas_db_repository.find(2023, RegistroProducao, "producao")

    assert result == ["converted"]


def test_remove_all_success(mock_session):
    query = mock_session.query.return_value
    filt2 = query.filter.return_value

    filt2.delete.return_value = 1

    op_internas_db_repository.remove_all("producao", session=mock_session)

    assert query.join.called
    assert query.filter.called
    assert filt2.delete.called


def test_remove_all_exception(mock_session):
    query = mock_session.query.return_value
    filt2 = query.filter.return_value

    filt2.delete.side_effect = Exception("Delete error")

    with pytest.raises(Exception, match="Delete error"):
        op_internas_db_repository.remove_all("producao", session=mock_session)
