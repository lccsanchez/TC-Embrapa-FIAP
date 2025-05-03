from sqlalchemy.orm import Session
from models import Processamentos, Registros
import pandas as pd
from scraper import agrupar_dados

def inserir_dados_no_banco(session: Session, df: pd.DataFrame):
    
    try:
        for _, row in df.iterrows():
            # Verificar se o registro de Processamentos já existe
            processamento = session.query(Processamentos).filter_by(
                cultivo=row["cultivar"]
            ).first()

            # Se não existir, criar um novo registro
            if not processamento:
                processamento = Processamentos(
                    cultivo=row["cultivar"],
                    categoria=row["categoria"],
                    classificacao=row["classificacao"],
                )
                session.add(processamento)
                session.flush()  # Garante que o ID do processamento seja gerado

            # Criar o registro de Registros
            registro = Registros(
                id_cultivo=processamento.id,
                ano=int(row["ano"]),
                quantidade=float(row["quantidade(kg)"]),
            )
            session.add(registro)

        session.commit()
        print("Dados inseridos com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao inserir dados no banco: {e}")

def processar_e_salvar_dados(session: Session, url: dict):
    
    df = agrupar_dados(url)
    if df is not None:
        inserir_dados_no_banco(session, df)


