import uuid
from models import Produto, RegistroProducao,Registros
from dto import ProducaoDto, RegistrosDto 

from sqlalchemy.orm import joinedload,with_loader_criteria
from app.database import SessionLocal  
from typing import List

session =SessionLocal()

def find_all():    
    producoes = session.query(RegistroProducao).all()
    
    return [model_to_dto(p) for p in producoes]
     

def find_by_year(year):
    subquery_ids = (
        session.query(Produto.id)
        .join(Produto.registros)
        .filter(RegistroProducao.ano == int(year) and RegistroProducao.tipo_operacao=='producao')
        .distinct()
        .subquery()
    )

    # Em seguida, buscar os Producao com seus filhos filtrados
    producoes = (
        session.query(Produto)
        .filter(Produto.id.in_(subquery_ids))
        .options(
            joinedload(Produto.registros),
            with_loader_criteria(Registros, Registros.ano == int(year) and Registros.tipo_operacao=="producao", include_aliases=True)
        )
        .all()
    )
   
    return [model_to_dto(p) for p in producoes]

def add_all(producoes: List[ProducaoDto]):  
    
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
    session.query(RegistroProducao).delete()

def dto_to_model(dto_obj: ProducaoDto) -> Produto:
     
    model = Produto(
        id=str(uuid.uuid4()),
        control=dto_obj.control,
        produto=dto_obj.produto
    )

    model.registros = [
        RegistroProducao(
            id=str(uuid.uuid4()), 
            tipo_operacao='producao',
            ano=ano.ano,           
            quantidade=ano.quantidade 
        )
        for ano in dto_obj.registros
    ]

    return model


def model_to_dto(model: Produto) -> ProducaoDto:
       
    produto_dto =ProducaoDto.model_validate(model)

    produto_dto.registros = [RegistrosDto.model_validate(r) for r in model.registros]

    return produto_dto.model_dump()
     
