from sqlalchemy import text
from app.database.session import engine


def test_database_connection():
    """Testa se a conexão com o banco de dados funciona corretamente."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
