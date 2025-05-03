from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import Base

db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)

    from routes import processamento, producao, comercio, auth, home
    app.register_blueprint(processamento)
    app.register_blueprint(producao)
    app.register_blueprint(comercio)
    app.register_blueprint(auth)
    app.register_blueprint(home)

    return app