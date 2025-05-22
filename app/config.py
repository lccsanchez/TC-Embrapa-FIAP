import os
from dotenv import load_dotenv #Usado para carregar variáveis de ambiente do arquivo .env
from urllib.parse import quote_plus

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da URL do banco de dados
DB_USER = os.getenv("DB_USER", "azureuser")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "your_password_here"))
DB_HOST = os.getenv("DB_HOST", "tcembrapadb.database.windows.net")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME", "tcembrapadb")

# String de conexão para Azure SQL com pyodbc
SQLALCHEMY_DATABASE_URI = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
)

SECRET_KEY = os.getenv("SECRET_KEY")