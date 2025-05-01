from flask import Flask, jsonify
from app.main import app
from app.scraper import gerar_json_agrupado
from app import urls

@app.route("/")
def home():
    return 'Bem Vindo à API de Dados da Vitivinicultura da Embrapa!'

@app.route("/processamento")
def get_processamento():
    return jsonify(gerar_json_agrupado(urls.urls_processamento))