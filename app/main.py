from flask import Flask, jsonify

app = Flask(__name__)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)