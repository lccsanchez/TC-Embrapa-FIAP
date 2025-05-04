from sqlalchemy.orm import Session
from app.models import User
import pandas as pd
from app.scraper import agrupar_dados

def inserir_usuario(session: Session, nickname: str, senha: str):
    try:
        # Verificar se o usuário já existe
        usuario_existente = session.query(User).filter_by(nickname=nickname).first()
        if usuario_existente:
            print(f"Usuário '{nickname}' já existe.")
            return

        # Criar um novo usuário
        novo_usuario = User(nickname=nickname, senha=senha)
        session.add(novo_usuario)
        session.commit()
        print(f"Usuário '{nickname}' inserido com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao inserir usuário: {e}")

