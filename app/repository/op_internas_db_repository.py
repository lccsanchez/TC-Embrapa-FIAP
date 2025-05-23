from sqlalchemy import and_
from app.model import Produto, Registros
from sqlalchemy.orm import joinedload, with_loader_criteria
from app.database import SessionLocal
from typing import List
from app.util import converter

def find(year: int, tipo_registro: type, opcao: str, subopcao: str = None):
    """
    Busca registros de Produto no banco de dados com base no ano, tipo de operação e classificação.
    """
    opcao = str.lower(opcao)
    subopcao = None if not subopcao else str(subopcao)

    filters = [ tipo_registro.ano == int(year), tipo_registro.tipo_operacao == opcao ] 

    if subopcao:
        filters.append(Produto.classificacao == subopcao)

    with SessionLocal() as session:
        subquery_ids = (
            session.query(Produto.id)
            .join(Produto.registros)
            .filter(
               and_(*filters)
            )
            .group_by(Produto.id, Produto.source_id)
            .order_by(Produto.source_id)
            .subquery()
        )

        filters = [Produto.id.in_(subquery_ids.select())]
        if subopcao:
            filters.append(Produto.classificacao == subopcao)

        producoes = (
            session.query(Produto)
            .filter(
                and_(*filters)
            )
            .options(
                joinedload(Produto.registros),
                with_loader_criteria(
                    Registros,
                    (Registros.ano == int(year)) & (Registros.tipo_operacao == opcao),
                    include_aliases=True
                )
            )
            .order_by(Produto.source_id)
            .all()
        )
        return converter.model_to_dto(producoes)

def add_all(nome_registro: str, items: List[Produto]):
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

def remove_all(nome_registro: str, session=None):
    """
    Remove todos os registros de Produto relacionados ao tipo de operação informado.
    """
    own_session = False
    if session is None:
        session = SessionLocal()
        own_session = True

    try:
        items = (
            session.query(Produto.id)
            .join(Registros)
            .filter(Registros.tipo_operacao == nome_registro)
            .subquery()
        )
        session.query(Produto)\
            .filter(Produto.id.in_(items.select()))\
            .delete(synchronize_session=False)
        if own_session:
            session.commit()
    except Exception as e:
        print(f"Erro no método remove_all: {e}")
        if own_session:
            session.rollback()
    finally:
        if own_session:
            session.close()
