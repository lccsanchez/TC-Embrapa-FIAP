import uuid
from models import Produto, RegistroProcessamento, Registros
from dto import ProcessamentoDto, RegistrosDto 
from sqlalchemy import and_

from sqlalchemy.orm import joinedload,with_loader_criteria
from app.database import SessionLocal  
from typing import List

session =SessionLocal()

def find_all():    
    processamentos = session.query(RegistroProcessamento).all()
   
    return [model_to_dto(p) for p in processamentos]
     

def find_by_year(year,classificacao):
    filters = [
        RegistroProcessamento.ano == int(year),
        RegistroProcessamento.tipo_operacao == 'processamentos'
    ]

    if classificacao:
        filters.append(Produto.classificacao == classificacao)

    subquery_ids = (
        session.query(Produto.id)
        .join(Produto.registros)
        .filter(and_(*filters))
        .distinct()
        .subquery()
    )

    # Em seguida, buscar os Producao com seus filhos filtrados
    processamento = (
        session.query(Produto)
        .filter(Produto.id.in_(subquery_ids))
        .options(
            joinedload(Produto.registros),
            with_loader_criteria(Registros, Registros.ano == int(year) and Registros.tipo_operacao=="processamentos", include_aliases=True)
        )
        .all()
    )
   
    return [model_to_dto(p) for p in processamento]

def add_all(producoes: List[ProcessamentoDto]):  
    
    try:
        remove_all()
        modelos = [dto_to_model(p) for p in producoes]       
        session.add_all(modelos)
        session.commit()
    except Exception as e:
            print(f"Erro no método add_all: {e}")    
            session.rollback()

    return producoes

def remove_all():
    session.query(RegistroProcessamento).delete()

def dto_to_model(dto_obj: ProcessamentoDto) -> Produto:
     
    model = Produto(
        id=str(uuid.uuid4()),
        control=dto_obj.control,
        produto=dto_obj.produto,
        classificacao=dto_obj.classificacao
    )

    model.registros = [
        RegistroProcessamento(
            id=str(uuid.uuid4()), 
            ano=ano.ano, 
            tipo_operacao="processamentos",         
            quantidade=ano.quantidade 
        )
        for ano in dto_obj.registros
    ]

    return model


def model_to_dto(model: Produto) -> ProcessamentoDto:
       
    produto_dto =ProcessamentoDto.model_validate(model)

    produto_dto.registros = [RegistrosDto.model_validate(r) for r in model.registros]

    return produto_dto.model_dump()
     
