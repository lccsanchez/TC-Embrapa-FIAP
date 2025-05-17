from app.model.entidades import Produto,Registros 
from sqlalchemy.orm import joinedload,with_loader_criteria
from app.database import SessionLocal  
from typing import List 
from util import converter
session =SessionLocal()  

def find_by_year(year):
    subquery_ids = (
        session.query(Produto.id)
        .join(Produto.registros)       
        .group_by(Produto.id, Produto.source_id) 
        .order_by(Produto.source_id) 
        .subquery()
    )

    producoes = (
        session.query(Produto)
        .filter(Produto.id.in_(subquery_ids))
        .options(
            joinedload(Produto.registros),
            with_loader_criteria(Registros, Registros.ano == int(year) and Registros.tipo_operacao=="producao", include_aliases=True)
        )
        .order_by(Produto.source_id) 
        .all()
    )
    
    return converter.model_to_dto(producoes)

def add_all(producoes: List[Produto]):  
    
    try:
        remove_all()          
        session.add_all(producoes)
        session.commit()
    except Exception as e:
            print(f"Erro no método add_all: {e}")    
            session.rollback()

    return producoes

def remove_all():
    produtos_com_producao = session.query(Produto.id)\
        .join(Registros)\
        .filter(Registros.tipo_operacao == 'producao')\
        .subquery()  
    
    session.query(Produto)\
        .filter(Produto.id.in_(produtos_com_producao))\
        .delete(synchronize_session=False)  
     
