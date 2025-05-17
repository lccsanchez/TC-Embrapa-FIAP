from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import Base

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    from routes import producao,processamento, importacao,exportacao, comercializacao
    app.register_blueprint(producao)
    app.register_blueprint(processamento)
    app.register_blueprint(comercializacao)
    app.register_blueprint(importacao)
    app.register_blueprint(exportacao)

    return app
