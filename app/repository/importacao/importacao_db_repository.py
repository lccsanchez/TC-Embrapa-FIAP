import uuid
from app.model.entidades import Pais, RegistroImportacao, RegistroImportacaoExportacao
from dto import ImportacaoDto, RegistrosImpExpDto

from sqlalchemy.orm import joinedload, with_loader_criteria
from app.database import SessionLocal
from typing import List

session = SessionLocal()

def find_all():    
    importacoes = session.query(RegistroImportacao).all()
    
    return [model_to_dto(p) for p in importacoes]

def find_by_year(year):
    subquery_ids = (
        session.query(Pais.id)
        .join(Pais.registros_imp_exp)
        .filter(
            RegistroImportacao.ano == int(year)
            and RegistroImportacao.tipo_operacao == "importacao"
        )
        .distinct()
        .subquery()
    )

    # Em seguida, buscar os Producao com seus filhos filtrados
    importacoes = (
        session.query(Pais)
        .filter(Pais.id.in_(subquery_ids))
        .options(
            joinedload(Pais.registros_imp_exp),
            with_loader_criteria(
                RegistroImportacaoExportacao,
                RegistroImportacao.ano == int(year)
                and RegistroImportacao.tipo_operacao == "importacao",
                include_aliases=True,
            ),
        )
        .all()
    )

    return [model_to_dto(p) for p in importacoes]


def add_all(importacoes: List[ImportacaoDto]):
    try:
        remove_all()
        modelos = [dto_to_model(p) for p in importacoes]       
        session.add_all(modelos)
        session.commit()
    except Exception as e:
            print(f"Erro no método add_all: {e}")    
            session.rollback()

    return importacoes

def remove_all():
    session.query(RegistroImportacao).delete()
    

def dto_to_model(dto_obj: ImportacaoDto) -> Pais:

    model = Pais(
        id=str(uuid.uuid4()),
        pais=dto_obj.pais
    )

    model.registros_imp_exp = [
        RegistroImportacao(
            id=str(uuid.uuid4()),
            tipo_operacao='importacao',
            ano=ano.ano,
            quantidade=ano.quantidade,
            valor=ano.valor
        )
        for ano in dto_obj.registros
    ]

    return model


def model_to_dto(model: Pais) -> ImportacaoDto:

    pais_dto = ImportacaoDto.model_validate(model)

    pais_dto.registros = [RegistrosImpExpDto.model_validate(r) for r in model.registros_imp_exp]

    return pais_dto.model_dump()

