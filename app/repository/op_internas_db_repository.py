from app.model import Produto,Registros 
from sqlalchemy.orm import joinedload,with_loader_criteria
from app.database import SessionLocal  
from typing import List 
from app.util import converter
session =SessionLocal()  

def find(year:int ,tipo_registro: type, opcao:str ,subopcao:str =None):
    opcao = str.lower(opcao)
    subopcao = None if not subopcao else str.lower(subopcao)
    subquery_ids = (
        session.query(Produto.id)
        .join(Produto.registros)       
        .filter(tipo_registro.ano == int(year) and tipo_registro.tipo_operacao==opcao and Produto.classificacao==subopcao)
        .group_by(Produto.id, Produto.source_id) 
        .order_by(Produto.source_id) 
        .subquery()
    )

    producoes = (
        session.query(Produto)
        .filter(Produto.id.in_(subquery_ids).__and__( Produto.classificacao==subopcao))
        .options(
            joinedload(Produto.registros),
            with_loader_criteria(Registros, Registros.ano == int(year) and Registros.tipo_operacao==opcao , include_aliases=True)
        )
        .order_by(Produto.source_id) 
        .all()
    )
    
    return converter.model_to_dto(producoes)

def add_all(nome_registro: str,items: List[Produto]):  
    
    try:
        remove_all(nome_registro)          
        session.add_all(items)
        session.commit()
    except Exception as e:
            print(f"Erro no método add_all: {e}")    
            session.rollback()

    return None

def remove_all(nome_registro):
    items = session.query(Produto.id)\
        .join(Registros)\
        .filter(Registros.tipo_operacao == nome_registro)\
        .subquery()  
    
    session.query(Produto)\
        .filter(Produto.id.in_(items))\
        .delete(synchronize_session=False)  
     
