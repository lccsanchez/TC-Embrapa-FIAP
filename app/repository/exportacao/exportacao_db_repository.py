import uuid
from models import Pais, RegistroExportacao, RegistroImportacaoExportacao
from dto import ExportacaoDto, RegistrosImpExpDto

from sqlalchemy.orm import joinedload, with_loader_criteria
from app.database import SessionLocal
from typing import List

session = SessionLocal()

def find_all():
    exportacoes = session.query(RegistroExportacao).all()

    return [model_to_dto(p) for p in exportacoes]

def find_by_year(year):
    subquery_ids = (
        session.query(Pais.id)
        .join(Pais.registros_imp_exp)
        .filter(
            RegistroExportacao.ano == int(year)
            and RegistroExportacao.tipo_operacao == "exportacao"
        )
        .distinct()
        .subquery()
    )

    # Em seguida, buscar os Producao com seus filhos filtrados
    exportacoes = (
        session.query(Pais)
        .filter(Pais.id.in_(subquery_ids))
        .options(
            joinedload(Pais.registros_imp_exp),
            with_loader_criteria(
                RegistroImportacaoExportacao,
                RegistroExportacao.ano == int(year)
                and RegistroExportacao.tipo_operacao == "exportacao",
                include_aliases=True,
            ),
        )
        .all()
    )

    return [model_to_dto(p) for p in exportacoes]


def add_all(exportacoes: List[ExportacaoDto]):
    try:
        remove_all()
        modelos = [dto_to_model(p) for p in exportacoes]
        session.add_all(modelos)
        session.commit()
    except Exception as e:
        print(f"Erro no método add_all: {e}")
        session.rollback()

    return exportacoes

def remove_all():
    session.query(RegistroExportacao).delete()


def dto_to_model(dto_obj: ExportacaoDto) -> Pais:

    model = Pais(
        id=str(uuid.uuid4()),
        pais=dto_obj.pais
    )

    model.registros_imp_exp = [
        RegistroExportacao(
            id=str(uuid.uuid4()),
            tipo_operacao="exportacao",
            ano=ano.ano,
            quantidade=ano.quantidade,
            valor=ano.valor
        )
        for ano in dto_obj.registros
    ]

    return model


def model_to_dto(model: Pais) -> ExportacaoDto:

    pais_dto = ExportacaoDto.model_validate(model)

    pais_dto.registros = [RegistrosImpExpDto.model_validate(r) for r in model.registros_imp_exp]

    return pais_dto.model_dump()
