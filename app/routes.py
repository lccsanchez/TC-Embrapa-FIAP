from flask import jsonify, Blueprint
from .scraper import gerar_json_agrupado
from .urls import urls_processamento

processamento = Blueprint('processamento', __name__)

@processamento.route("/")
def home():
    return 'Bem Vindo à API de Dados da Vitivinicultura da Embrapa!'

@processamento.route("/processamento")
def get_processamento():
    return jsonify(gerar_json_agrupado(urls_processamento))