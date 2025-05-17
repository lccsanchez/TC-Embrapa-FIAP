import uuid
from app.model.entidades import Produto, RegistroComercio,Registros
from dto import ComercioDto, RegistrosDto 

from sqlalchemy.orm import joinedload,with_loader_criteria
from app.database import SessionLocal  
from typing import List

session =SessionLocal()

def find_all():    
    comercios = session.query(RegistroComercio).all()
    
    return [model_to_dto(p) for p in comercios]
     

def find_by_year(year):
    subquery_ids = (
        session.query(Produto.id)
        .join(Produto.registros)
        .filter(RegistroComercio.ano == int(year) and RegistroComercio.tipo_operacao=='comercio')
        .distinct()
        .subquery()
    )

    # Em seguida, buscar os Comercio com seus filhos filtrados
    comercios = (
        session.query(Produto)
        .filter(Produto.id.in_(subquery_ids))
        .options(
            joinedload(Produto.registros),
            with_loader_criteria(Registros, Registros.ano == int(year) and Registros.tipo_operacao=="comercio", include_aliases=True)
        )
        .all()
    )
   
    return [model_to_dto(p) for p in comercios]

def add_all(comercios: List[ComercioDto]):  
    
    try:
        remove_all()
        modelos = [dto_to_model(p) for p in comercios]       
        session.add_all(modelos)
        session.commit()
    except Exception as e:
            print(f"Erro no método add_all: {e}")    
            session.rollback()

    return comercios

def remove_all():
    session.query(RegistroComercio).delete()

def dto_to_model(dto_obj: ComercioDto) -> Produto:
     
    model = Produto(
        id=str(uuid.uuid4()),
        control=dto_obj.control,
        produto=dto_obj.produto
    )

    model.registros = [
        RegistroComercio(
            id=str(uuid.uuid4()), 
            tipo_operacao='comercio',
            ano=ano.ano,           
            quantidade=ano.quantidade 
        )
        for ano in dto_obj.registros
    ]

    return model


def model_to_dto(model: Produto) -> ComercioDto:
       
    produto_dto =ComercioDto.model_validate(model)

    produto_dto.registros = [RegistrosDto.model_validate(r) for r in model.registros]

    return produto_dto.model_dump()
     
