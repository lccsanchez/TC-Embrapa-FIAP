import os
from dotenv import load_dotenv #Usado para carregar variáveis de ambiente do arquivo .env
from urllib.parse import quote_plus

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da URL do banco de dados
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME", "tcembrapadb")

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = os.getenv("SECRET_KEY")