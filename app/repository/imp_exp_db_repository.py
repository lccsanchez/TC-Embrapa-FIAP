from app.model import ImportacaoExportacao, RegistroImportacaoExportacao
from sqlalchemy.orm import joinedload, with_loader_criteria
from app.database import SessionLocal
from typing import List
from app.util import converter

session = SessionLocal()


def find(year: int, tipo_registro: type, opcao: str, subopcao: str = None):
    opcao = str.lower(opcao)
    subopcao = str.lower(subopcao)
    subquery_ids = (
        session.query(ImportacaoExportacao.id)
        .join(ImportacaoExportacao.RegistroImportacaoExportacao)
        .filter(
            tipo_registro.ano == int(year)
            and tipo_registro.tipo_operacao == opcao
            and ImportacaoExportacao.classificacao == subopcao
        )
        .group_by(ImportacaoExportacao.id, ImportacaoExportacao.source_id)
        .subquery()
    )

    importacoes = (
        session.query(ImportacaoExportacao)
        .filter(ImportacaoExportacao.id.in_(subquery_ids).__and__(ImportacaoExportacao.classificacao == subopcao))
        .options(
            joinedload(ImportacaoExportacao.RegistroImportacaoExportacao),
            with_loader_criteria(
                RegistroImportacaoExportacao,
                RegistroImportacaoExportacao.ano == int(year) and RegistroImportacaoExportacao.tipo_operacao == opcao,
                include_aliases=True,
            ),
        )
        .order_by(ImportacaoExportacao.source_id)
        .all()
    )

    return converter.model_to_dto(importacoes)


def add_all(nome_registro: str, items: List[ImportacaoExportacao]):

    try:
        remove_all(nome_registro)
        session.add_all(items)
        print(items)
        session.commit()
    except Exception as e:
        print(f"Erro no método add_all: {e}")
        session.rollback()

    return None


def remove_all(nome_registro):
    items = (
        session.query(ImportacaoExportacao.id)
        .join(RegistroImportacaoExportacao)
        .filter(RegistroImportacaoExportacao.tipo_operacao == nome_registro)
        .subquery()
    )

    session.query(ImportacaoExportacao).filter(ImportacaoExportacao.id.in_(items)).delete(
        synchronize_session=False
    )
