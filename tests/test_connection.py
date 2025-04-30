from sqlalchemy import text
from app.database import engine

# Testa a conexão com o banco de dados
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexão bem-sucedida:", result.fetchone())
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)