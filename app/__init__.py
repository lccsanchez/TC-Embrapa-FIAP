from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import Base

db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)

    from .routes import processamento
    app.register_blueprint(processamento)

    return app