from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import Base

app = Flask(__name__)

db = SQLAlchemy(app, model_class=Base)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)