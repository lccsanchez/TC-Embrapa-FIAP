from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import Base

# Inicializa o Flask e o SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app, model_class=Base)

# Importa os módulos para registrar rotas e modelos
from app import routes