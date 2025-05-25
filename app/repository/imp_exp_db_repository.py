"""Repositório para operações de ImportacaoExportacao no banco de dados."""

from typing import List
from sqlalchemy.orm import aliased, contains_eager
from sqlalchemy import func
from app.model.model import ImportacaoExportacao, RegistroImportacaoExportacao
from app.database.session import SessionLocal
from app.util import converter


def find(year: int, opcao: str, subopcao: str = None):
    """
    Busca registros de ImportacaoExportacao no banco de dados com base no ano,
    tipo de operação e classificação.
    """
    opcao = opcao.lower() if opcao else ""
    subopcao = subopcao.lower() if subopcao else None

    with SessionLocal() as session:
        registro_alias = aliased(RegistroImportacaoExportacao)

        subquery_ids = (
            session.query(ImportacaoExportacao.id)
            .join(registro_alias, registro_alias.id_pais == ImportacaoExportacao.id)
            .filter(
                registro_alias.ano == year,
                func.lower(registro_alias.tipo_operacao) == opcao,
                ImportacaoExportacao.classificacao == subopcao,
            )
            .group_by(ImportacaoExportacao.id, ImportacaoExportacao.source_id)
            .subquery()
        )

        registro_join = aliased(RegistroImportacaoExportacao)

        importacoes = (
            session.query(ImportacaoExportacao)
            .join(registro_join, registro_join.id_pais == ImportacaoExportacao.id)
            .filter(
                ImportacaoExportacao.id.in_(subquery_ids),
                registro_join.ano == year,
                func.lower(registro_join.tipo_operacao) == opcao,
            )
            .options(
                contains_eager(
                    ImportacaoExportacao.registros_imp_exp, alias=registro_join
                )
            )
            .order_by(ImportacaoExportacao.source_id)
            .all()
        )

        return converter.imp_exp_to_dto(importacoes)


def add_all(nome_registro: str, items: List[ImportacaoExportacao]):
    """
    Remove registros anteriores e insere nova lista.
    """
    try:
        with SessionLocal() as session:
            remove_all(nome_registro, session)
            session.add_all(items)
            session.commit()
    except Exception as e:
        print(f"Erro no método add_all: {e}")
        raise


def remove_all(nome_registro: str, session=None):
    """
    Remove todos os registros de ImportacaoExportacao relacionados ao
    tipo de operação informado.
    """
    own_session = False
    if session is None:
        session = SessionLocal()
        own_session = True

    try:
        subquery_ids = (
            session.query(ImportacaoExportacao.id)
            .join(RegistroImportacaoExportacao)
            .filter(RegistroImportacaoExportacao.tipo_operacao == nome_registro)
            .subquery()
        )

        session.query(ImportacaoExportacao).filter(
            ImportacaoExportacao.id.in_(subquery_ids)
        ).delete(synchronize_session=False)

        if own_session:
            session.commit()

    except Exception as e:
        print(f"Erro no método remove_all: {e}")
        if own_session:
            session.rollback()
        raise
    finally:
        if own_session:
            session.close()
