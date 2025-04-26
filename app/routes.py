from flask import Flask, jsonify
from main import app
from scraper import gerar_json_agrupado
from urls import urls_processamento

@app.route("/")
def home():
    return 'Bem Vindo à API de Dados da Vitivinicultura da Embrapa!'

@app.route("/processamento")
def get_processamento():
    return jsonify(gerar_json_agrupado(urls_processamento))