import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER", "azureuser")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST", "tcembrapadb.mysql.database.azure.com")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "tcembrapadb")
SSL_CA = os.getenv("SSL_CA", "certs/DigiCertGlobalRootCA.crt.pem")

# String de conexão para Azure MySQL com pymysql
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?ssl_ca={SSL_CA}"
)

SECRET_KEY = os.getenv("SECRET_KEY")

##-- C:\desenv\python\tcembrapa-atual\TC-Embrapa-FIAP\certs\DigiCertGlobalRootCA.crt.pem"